# Celery Integration Guide

## Overview

This project now includes **Celery** distributed task queue for handling long-running model training operations asynchronously. This allows the API to respond immediately while training continues in the background.

## Architecture

```
┌──────────────┐
│   Frontend   │ (Next.js on :3000)
│   (Browser)  │
└──────┬───────┘
       │ HTTP Requests
       ▼
┌──────────────┐
│   Frontend   │ (Next.js Server)
│    Server    │
└──────┬───────┘
       │ Proxy API Calls
       ▼
┌──────────────┐      ┌─────────────┐
│   FastAPI    │◄────►│    Redis    │ (Message Broker)
│   Backend    │      │   (:6379)   │
└──────┬───────┘      └──────┬──────┘
       │                     │
       │ Submit Tasks        │ Consume Tasks
       ▼                     ▼
┌──────────────┐      ┌─────────────┐
│    Flower    │      │   Celery    │
│  Monitoring  │      │   Worker    │
│   (:5555)    │      │             │
└──────────────┘      └─────────────┘
```

## Components

### 1. **Redis** (Message Broker & Result Backend)
- Stores task queue (pending tasks)
- Stores task results and progress
- Lightweight and fast
- Port: `6379`

### 2. **FastAPI Backend**
- Submits training tasks to Celery
- Provides endpoints to check task status
- Returns results when tasks complete
- Port: `5000`

### 3. **Celery Worker**
- Consumes tasks from Redis queue
- Executes long-running training operations
- Reports progress back to Redis
- Can scale horizontally (multiple workers)

### 4. **Flower** (Monitoring UI)
- Web-based monitoring dashboard
- View active/completed tasks
- Monitor worker status
- Inspect task details
- Port: `5555`

### 5. **Next.js Frontend**
- Submits training requests
- Polls for task status every 2 seconds
- Displays progress bar
- Shows real-time updates
- Port: `3000`

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Start all services
docker-compose up --build

# Or use the convenience scripts:
# Windows:
start-all.bat

# Linux/Mac:
chmod +x start-all.sh
./start-all.sh
```

### Option 2: Manual Setup (Development)

**Terminal 1 - Redis:**
```bash
redis-server
```

**Terminal 2 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python api.py
```

**Terminal 3 - Celery Worker:**
```bash
cd backend
celery -A celery_app worker --loglevel=info
```

**Terminal 4 - Flower (Optional):**
```bash
cd backend
celery -A celery_app flower --port=5555
```

**Terminal 5 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### Asynchronous Training Endpoints

#### Submit Training Task
```http
POST /train/{model_type}/async
```

**Parameters:**
- `model_type`: `tensorflow`, `pytorch`, `xgboost`, or `all`

**Request Body:**
```json
{
  "epochs": 500,
  "learning_rate": 0.001,
  "hidden_sizes": [64, 32, 16]
}
```

**Response:**
```json
{
  "success": true,
  "task_id": "3c4e6a8b-7f2d-4a1e-9b5c-8d3f6e2a1b4c",
  "message": "Training task submitted for tensorflow",
  "model_type": "tensorflow"
}
```

#### Check Task Status
```http
GET /task/{task_id}/status
```

**Response:**
```json
{
  "task_id": "3c4e6a8b-7f2d-4a1e-9b5c-8d3f6e2a1b4c",
  "state": "PROGRESS",
  "progress": {
    "current": 250,
    "total": 500,
    "percent": 50,
    "message": "Training epoch 250/500"
  }
}
```

**Task States:**
- `PENDING`: Task waiting to start
- `STARTED`: Task has begun execution
- `PROGRESS`: Task in progress (with progress info)
- `SUCCESS`: Task completed successfully
- `FAILURE`: Task failed with error

#### Get Task Result
```http
GET /task/{task_id}/result
```

**Response (Success):**
```json
{
  "success": true,
  "state": "SUCCESS",
  "result": {
    "success": true,
    "message": "TENSORFLOW model trained successfully",
    "model_type": "tensorflow",
    "metrics": {
      "train_r2": 0.85,
      "test_r2": 0.83,
      "train_rmse": 0.45,
      "test_rmse": 0.48,
      "final_loss": 0.032
    }
  }
}
```

#### Check Celery Worker Health
```http
GET /celery/health
```

**Response:**
```json
{
  "success": true,
  "celery_status": "connected",
  "worker_response": {
    "status": "healthy",
    "message": "Celery worker is operational"
  }
}
```

### Synchronous Training (Legacy)

The original synchronous endpoints are still available:

```http
POST /train/{model_type}
```

These block until training completes (not recommended for long training sessions).

## Frontend Usage

### Model Training Flow

1. **User selects model type:**
   - TensorFlow
   - PyTorch
   - Hugging Face
   - All Models (trains all three)

2. **User clicks "Train Model":**
   - Request sent to `/api/train`
   - Backend returns `task_id` immediately
   - UI shows "Task submitted"

3. **Polling begins:**
   - Frontend polls `/api/task/{task_id}` every 2 seconds
   - Progress bar updates in real-time
   - Shows current status message

4. **Training completes:**
   - Final metrics displayed
   - Model ready for predictions
   - Polling stops automatically

### Progress Updates

The progress bar shows:
- **0%**: Task submitted, waiting to start
- **1-99%**: Training in progress (epoch progress)
- **100%**: Training complete

## Flower Monitoring Dashboard

Access Flower at `http://localhost:5555` to:

- **Tasks Tab**: View all tasks (active, succeeded, failed)
- **Workers Tab**: Monitor worker processes
- **Broker Tab**: Check Redis connection
- **Task Details**: Click any task to see:
  - Task arguments
  - Execution time
  - Result or error
  - Stack trace (if failed)

## Configuration

### Environment Variables

**Backend:**
```bash
REDIS_URL=redis://localhost:6379/0
PORT=5000
```

**Frontend:**
```bash
BACKEND_URL=http://localhost:5000
NODE_ENV=production
```

### Celery Configuration

Edit `backend/celery_app.py`:

```python
celery_app.conf.update(
    task_time_limit=3600,        # 1 hour max
    worker_prefetch_multiplier=1, # Tasks per worker
    worker_max_tasks_per_child=10 # Restart after N tasks
)
```

## Scaling

### Horizontal Scaling (Multiple Workers)

Run multiple Celery workers to handle concurrent training:

```bash
# Worker 1
celery -A celery_app worker -n worker1@%h --loglevel=info

# Worker 2 (separate terminal)
celery -A celery_app worker -n worker2@%h --loglevel=info

# Worker 3 (separate terminal)
celery -A celery_app worker -n worker3@%h --loglevel=info
```

With Docker Compose:
```bash
docker-compose up --scale celery-worker=3
```

### GPU Support

Assign specific GPUs to workers:

```bash
CUDA_VISIBLE_DEVICES=0 celery -A celery_app worker -n gpu0@%h
CUDA_VISIBLE_DEVICES=1 celery -A celery_app worker -n gpu1@%h
```

## Troubleshooting

### Celery Worker Not Starting

**Check Redis connection:**
```bash
redis-cli ping
# Should return: PONG
```

**Check worker logs:**
```bash
celery -A celery_app worker --loglevel=debug
```

### Tasks Stuck in PENDING

**Possible causes:**
1. Worker not running
2. Redis not accessible
3. Task name mismatch

**Solution:**
```bash
# Check worker status
celery -A celery_app inspect active

# Restart worker
docker-compose restart celery-worker
```

### Task Failed with Error

**View error in Flower:**
1. Open `http://localhost:5555`
2. Click "Tasks" tab
3. Find failed task
4. View traceback

**Check worker logs:**
```bash
docker-compose logs celery-worker
```

### Redis Connection Error

**Verify Redis is running:**
```bash
docker ps | grep redis
```

**Check Redis logs:**
```bash
docker-compose logs redis
```

## Performance Tips

1. **Adjust polling interval:**
   - Default: 2 seconds
   - Edit `frontend/components/TrainingPanel.tsx`
   - Change `setInterval` duration

2. **Increase worker concurrency:**
   ```bash
   celery -A celery_app worker --concurrency=4
   ```

3. **Use Redis persistence:**
   - Already configured in `docker-compose.yml`
   - Uses AOF (Append-Only File)

4. **Monitor memory usage:**
   - Long training sessions consume memory
   - Workers restart after 10 tasks (configured)

## Learning Resources

### Celery Concepts

**Producer (FastAPI):**
- Submits tasks to queue
- Doesn't wait for completion
- Returns task ID immediately

**Broker (Redis):**
- Stores task queue
- Distributes tasks to workers
- Stores task results

**Consumer (Celery Worker):**
- Picks tasks from queue
- Executes tasks
- Reports progress and results

**Result Backend (Redis):**
- Stores task state and results
- Allows status queries
- Expires old results (1 hour default)

### Task States Flow

```
PENDING → STARTED → PROGRESS → SUCCESS
                              ↘ FAILURE
```

### Why Celery?

1. **Non-blocking**: API responds immediately
2. **Scalable**: Add workers as needed
3. **Reliable**: Tasks persist in Redis
4. **Monitorable**: Flower provides visibility
5. **Retryable**: Failed tasks can auto-retry
6. **Distributed**: Workers can run on different machines

## Next Steps

1. **Add retry logic:**
   ```python
   @celery_app.task(bind=True, max_retries=3)
   def train_model_async(self, ...):
       try:
           # training code
       except Exception as exc:
           raise self.retry(exc=exc, countdown=60)
   ```

2. **Add task prioritization:**
   ```python
   task.apply_async(args=[...], priority=5)
   ```

3. **Schedule periodic tasks:**
   ```python
   from celery.schedules import crontab
   
   celery_app.conf.beat_schedule = {
       'retrain-models-daily': {
           'task': 'tasks.train_all_models',
           'schedule': crontab(hour=2, minute=0),
       },
   }
   ```

4. **Add email notifications:**
   ```python
   @celery_app.task
   def send_training_complete_email(email, metrics):
       # Send email with results
   ```

## Port Reference

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3000 | Next.js web interface |
| Backend | 5000 | FastAPI REST API |
| Redis | 6379 | Message broker & result backend |
| Flower | 5555 | Celery monitoring dashboard |

## Additional Commands

**View active tasks:**
```bash
celery -A celery_app inspect active
```

**View registered tasks:**
```bash
celery -A celery_app inspect registered
```

**Purge all tasks:**
```bash
celery -A celery_app purge
```

**Stop workers gracefully:**
```bash
celery -A celery_app control shutdown
```

---

**Happy distributed training! 🚀**


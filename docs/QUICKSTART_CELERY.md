# Quick Start: Celery + Docker Setup

## TL;DR - Get Running in 2 Minutes

```bash
# Clone/Navigate to project
cd ai-deep-learning-example

# Start everything with Docker
docker-compose up --build

# Or use convenience script:
# Windows:
start-all.bat

# Linux/Mac:
chmod +x start-all.sh && ./start-all.sh
```

**That's it!** 🎉

Wait 2-3 minutes for services to start, then access:
- **App**: http://localhost:3000
- **API Docs**: http://localhost:5000/docs
- **Celery Monitor**: http://localhost:5555

## What You Get

✅ **Redis** - Message broker running  
✅ **FastAPI Backend** - API server ready  
✅ **Celery Worker** - Task processor active  
✅ **Flower** - Monitoring dashboard live  
✅ **Next.js Frontend** - Web UI loaded  

## Test It Out

### 1. Open Frontend
Visit http://localhost:3000

### 2. Train a Model (Async)
- Select model type: TensorFlow
- Set epochs: 500
- Click **"Train Model (Async with Celery)"**
- Get task ID immediately
- Watch progress bar update in real-time

### 3. Monitor with Flower
Open http://localhost:5555
- See your task in "Tasks" tab
- Watch worker status
- View task details

### 4. Make Predictions
After training completes:
- Fill in house details
- Click "Predict Price"
- Get instant prediction

## Key Features Explained

### Before Celery ❌
```
User → Submit Train Request → Wait 3 minutes... → Get Result
         (Browser frozen, no feedback)
```

### With Celery ✅
```
User → Submit Train Request → Get Task ID (instant!)
         ↓
     Poll Status Every 2s
         ↓
     See Progress Bar (0% → 100%)
         ↓
     Training happens in background
         ↓
     Get Results When Done
```

## Architecture in Simple Terms

```
┌─────────┐
│ Browser │ (You)
└────┬────┘
     │ "Train model please"
     ▼
┌─────────┐
│ FastAPI │ "OK, task ID: abc123"
└────┬────┘ (Returns immediately)
     │
     │ Puts task in queue ▼
               ┌───────┐
               │ Redis │ (Queue)
               └───┬───┘
                   │
                   │ Worker picks task ▼
               ┌─────────┐
               │ Celery  │ "I'll do it!"
               │ Worker  │ (Trains model)
               └─────────┘
```

**You**: Poll "Is abc123 done?"  
**FastAPI**: Checks Redis → "50% complete"  
**You**: Poll again...  
**FastAPI**: Checks Redis → "100% done! Here are results"  

## Common Tasks

### Stop Services
```bash
# Ctrl+C in terminal
# Then:
docker-compose down
```

### View Logs
```bash
docker-compose logs -f celery-worker
```

### Restart Worker (after code changes)
```bash
docker-compose restart celery-worker
```

### Train All Models
1. Select "All Models" in dropdown
2. Click train
3. Wait ~5-10 minutes
4. See results for all 3 models

### Scale Workers (handle multiple requests)
```bash
docker-compose up --scale celery-worker=3
```

Now you can train 3 models simultaneously!

## API Testing (Optional)

### Using curl

**Submit Task:**
```bash
curl -X POST http://localhost:5000/train/tensorflow/async \
  -H "Content-Type: application/json" \
  -d '{"epochs": 100}'
```

**Response:**
```json
{
  "success": true,
  "task_id": "abc123...",
  "message": "Training task submitted"
}
```

**Check Status:**
```bash
curl http://localhost:5000/task/abc123.../status
```

**Response:**
```json
{
  "task_id": "abc123...",
  "state": "PROGRESS",
  "progress": {
    "percent": 50,
    "message": "Training epoch 50/100"
  }
}
```

### Using Python

```python
import requests
import time

# Submit task
response = requests.post('http://localhost:5000/train/tensorflow/async', 
                         json={'epochs': 100})
task_id = response.json()['task_id']
print(f"Task ID: {task_id}")

# Poll status
while True:
    status = requests.get(f'http://localhost:5000/task/{task_id}/status').json()
    print(f"State: {status['state']}, Progress: {status.get('progress', {}).get('percent', 0)}%")
    
    if status['state'] in ['SUCCESS', 'FAILURE']:
        break
    
    time.sleep(2)

# Get result
result = requests.get(f'http://localhost:5000/task/{task_id}/result').json()
print("Result:", result)
```

## Troubleshooting

### "Cannot connect to backend"
**Wait 30 seconds** - Services need time to start

Still failing?
```bash
docker-compose logs backend
```

### "Redis connection refused"
```bash
docker-compose restart redis
docker-compose restart celery-worker
```

### "Task stuck in PENDING"
```bash
# Worker might be down
docker-compose ps celery-worker

# Restart it
docker-compose restart celery-worker
```

### Flower shows no workers
```bash
# Check worker logs
docker-compose logs celery-worker

# Should see: "celery@hostname ready"
```

## Next Steps

1. **Read Full Docs:**
   - `CELERY_INTEGRATION.md` - Detailed Celery guide
   - `DOCKER_SETUP.md` - Docker deep dive

2. **Experiment:**
   - Train different models
   - Compare results
   - Monitor with Flower

3. **Modify Code:**
   - Edit `backend/celery_tasks.py`
   - Add new async tasks
   - Restart worker to test

4. **Production:**
   - Add authentication
   - Set up SSL
   - Configure monitoring

## Learning Goals

By using this setup, you'll learn:

- ✅ **Message Queues**: How Redis stores tasks
- ✅ **Async Processing**: Non-blocking operations
- ✅ **Distributed Systems**: Multiple workers
- ✅ **Monitoring**: Flower dashboards
- ✅ **Docker Compose**: Multi-container apps
- ✅ **API Design**: Async endpoints

## Useful Commands Cheat Sheet

```bash
# Start
docker-compose up

# Start in background
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f [service]

# Restart service
docker-compose restart [service]

# Scale workers
docker-compose up --scale celery-worker=3

# Execute command
docker-compose exec backend python train.py

# Check status
docker-compose ps

# Clean up
docker-compose down -v
```

## URLs Reference

| What | Where |
|------|-------|
| Main App | http://localhost:3000 |
| API Docs | http://localhost:5000/docs |
| API Health | http://localhost:5000/health |
| Celery Health | http://localhost:5000/celery/health |
| Flower Monitor | http://localhost:5555 |

## Support

**Issues?** Check:
1. Docker is running
2. Ports are available (3000, 5000, 5555, 6379)
3. Logs: `docker-compose logs`

**Still stuck?** 
- Check `DOCKER_SETUP.md` troubleshooting section
- Review `CELERY_INTEGRATION.md` for detailed explanations

---

**Happy async training! 🚀**


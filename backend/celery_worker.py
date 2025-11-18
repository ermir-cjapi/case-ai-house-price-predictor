"""
Celery tasks for asynchronous model training
Implements training tasks with progress tracking and status updates
"""
from celery import Task
from celery_config import celery_app
from services.training_service import HousePriceModel
import traceback


class ProgressTrackingTask(Task):
    """Base task class with progress tracking capabilities"""
    
    def update_progress(self, current, total, message=""):
        """Update task progress"""
        percent = int((current / total) * 100) if total > 0 else 0
        self.update_state(
            state='PROGRESS',
            meta={
                'current': current,
                'total': total,
                'percent': percent,
                'message': message
            }
        )


@celery_app.task(bind=True, base=ProgressTrackingTask, name='celery_worker.train_model_async')
def train_model_async(self, model_type: str, epochs: int = 500, 
                      learning_rate: float = 0.001, 
                      hidden_sizes: list = None):
    """
    Asynchronous model training task with progress tracking
    
    Args:
        model_type: Type of model to train ('tensorflow', 'pytorch', 'xgboost', 'all')
        epochs: Number of training epochs
        learning_rate: Learning rate for optimizer
        hidden_sizes: Hidden layer sizes
        
    Returns:
        Dictionary with training results and metrics
    """
    if hidden_sizes is None:
        hidden_sizes = [64, 32, 16]
    
    try:
        # Update state to STARTED
        self.update_state(state='STARTED', meta={'message': 'Initializing training...'})
        
        if model_type == 'all':
            # Train all models
            model_types = ['tensorflow', 'pytorch', 'xgboost']
            total_models = len(model_types)
            results = {}
            
            for idx, mt in enumerate(model_types):
                self.update_progress(
                    current=idx,
                    total=total_models,
                    message=f'Training {mt.upper()} model ({idx + 1}/{total_models})...'
                )
                
                model = HousePriceModel(model_type=mt)
                metrics = model.train_model(
                    epochs=epochs,
                    learning_rate=learning_rate,
                    hidden_sizes=hidden_sizes
                )
                results[mt] = metrics
            
            # Don't update to 100% - let Celery handle SUCCESS state
            
            return {
                'success': True,
                'message': 'All models trained successfully',
                'model_type': 'all',
                'results': results
            }
        else:
            # Train specific model
            self.update_progress(
                current=0,
                total=epochs,
                message=f'Starting {model_type.upper()} model training...'
            )
            
            model = HousePriceModel(model_type=model_type)
            
            # Train the model
            self.update_progress(
                current=0,
                total=epochs,
                message=f'Training {model_type.upper()} model...'
            )
            
            metrics = model.train_model(
                epochs=epochs,
                learning_rate=learning_rate,
                hidden_sizes=hidden_sizes
            )
            
            # Don't update progress to 100% - let Celery set SUCCESS state automatically
            # when the function returns successfully
            
            return {
                'success': True,
                'message': f'{model_type.upper()} model trained successfully',
                'model_type': model_type,
                'metrics': metrics
            }
    
    except Exception as e:
        # Capture error details
        error_message = str(e)
        error_traceback = traceback.format_exc()
        
        self.update_state(
            state='FAILURE',
            meta={
                'error': error_message,
                'traceback': error_traceback
            }
        )
        
        raise Exception(f"Training failed: {error_message}")


@celery_app.task(name='celery_worker.health_check')
def health_check():
    """Simple health check task to verify Celery worker is running"""
    return {'status': 'healthy', 'message': 'Celery worker is operational'}


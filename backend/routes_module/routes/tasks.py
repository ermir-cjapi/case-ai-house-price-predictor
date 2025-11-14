"""
Asynchronous task status and result endpoints
"""
from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from schemas.task import TaskStatusResponse
from celery_config import celery_app

router = APIRouter()


@router.get("/task/{task_id}/status", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    Get the status of an asynchronous task
    
    Returns task state and progress information
    
    States:
        - PENDING: Task is waiting to be executed
        - STARTED: Task has started executing
        - PROGRESS: Task is in progress (with progress info)
        - SUCCESS: Task completed successfully
        - FAILURE: Task failed with error
    """
    try:
        task_result = AsyncResult(task_id, app=celery_app)
        
        response = {
            'task_id': task_id,
            'state': task_result.state,
            'progress': None,
            'result': None,
            'error': None
        }
        
        if task_result.state == 'PENDING':
            response['progress'] = {
                'current': 0,
                'total': 100,
                'percent': 0,
                'message': 'Task is waiting to start...'
            }
        
        elif task_result.state == 'STARTED':
            response['progress'] = {
                'current': 0,
                'total': 100,
                'percent': 0,
                'message': 'Task has started...'
            }
        
        elif task_result.state == 'PROGRESS':
            response['progress'] = task_result.info
        
        elif task_result.state == 'SUCCESS':
            response['result'] = task_result.result
            response['progress'] = {
                'current': 100,
                'total': 100,
                'percent': 100,
                'message': 'Training completed successfully!'
            }
        
        elif task_result.state == 'FAILURE':
            error_info = task_result.info
            response['error'] = str(error_info) if error_info else 'Unknown error'
            response['progress'] = {
                'current': 0,
                'total': 100,
                'percent': 0,
                'message': 'Training failed'
            }
        
        return TaskStatusResponse(**response)
    
    except Exception as e:
        print(f"Error getting task status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get task status: {str(e)}"
        )


@router.get("/task/{task_id}/result")
async def get_task_result(task_id: str):
    """
    Get the result of a completed task
    
    Returns the full result if task is completed successfully,
    otherwise returns status information
    """
    try:
        task_result = AsyncResult(task_id, app=celery_app)
        
        if task_result.state == 'SUCCESS':
            return {
                'success': True,
                'state': 'SUCCESS',
                'result': task_result.result
            }
        elif task_result.state == 'FAILURE':
            return {
                'success': False,
                'state': 'FAILURE',
                'error': str(task_result.info)
            }
        else:
            return {
                'success': False,
                'state': task_result.state,
                'message': f'Task is not yet completed. Current state: {task_result.state}'
            }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get task result: {str(e)}"
        )


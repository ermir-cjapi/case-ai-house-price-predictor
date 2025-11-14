'use client'

import { useState, useEffect, useRef } from 'react'

interface TrainingPanelProps {
  onTrainingComplete: () => void
}

interface TrainingMetrics {
  train_r2: number
  test_r2: number
  train_rmse: number
  test_rmse: number
  final_loss: number
}

interface TaskProgress {
  current: number
  total: number
  percent: number
  message: string
}

interface TaskStatus {
  task_id: string
  state: string
  progress?: TaskProgress
  result?: {
    success: boolean
    message: string
    model_type: string
    metrics?: TrainingMetrics
    results?: Record<string, { metrics: TrainingMetrics }>
  }
  error?: string
}

export default function TrainingPanel({ onTrainingComplete }: TrainingPanelProps) {
  const [training, setTraining] = useState(false)
  const [metrics, setMetrics] = useState<TrainingMetrics | null>(null)
  const [allMetrics, setAllMetrics] = useState<Record<string, TrainingMetrics> | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [epochs, setEpochs] = useState('500')
  const [modelType, setModelType] = useState('tensorflow')
  const [taskId, setTaskId] = useState<string | null>(null)
  const [progress, setProgress] = useState<TaskProgress | null>(null)
  const pollInterval = useRef<NodeJS.Timeout | null>(null)

  // Poll for task status
  const pollTaskStatus = async (id: string) => {
    try {
      const response = await fetch(`/api/task/${id}`)
      const data: TaskStatus = await response.json()

      // Update progress
      if (data.progress) {
        setProgress(data.progress)
      }

      // Check if task is complete
      if (data.state === 'SUCCESS') {
        setTraining(false)
        if (pollInterval.current) {
          clearInterval(pollInterval.current)
          pollInterval.current = null
        }

        // Extract metrics
        if (data.result) {
          if (data.result.model_type === 'all' && data.result.results) {
            // Multiple models trained
            const metricsMap: Record<string, TrainingMetrics> = {}
            Object.entries(data.result.results).forEach(([key, value]) => {
              metricsMap[key] = value.metrics
            })
            setAllMetrics(metricsMap)
          } else if (data.result.metrics) {
            // Single model trained
            setMetrics(data.result.metrics)
          }
        }

        setProgress({
          current: 100,
          total: 100,
          percent: 100,
          message: 'Training completed successfully!'
        })
        onTrainingComplete()
      } else if (data.state === 'FAILURE') {
        setTraining(false)
        if (pollInterval.current) {
          clearInterval(pollInterval.current)
          pollInterval.current = null
        }
        setError(data.error || 'Training failed with unknown error')
      }
    } catch (err) {
      console.error('Error polling task status:', err)
    }
  }

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (pollInterval.current) {
        clearInterval(pollInterval.current)
      }
    }
  }, [])

  const handleTrain = async () => {
    setTraining(true)
    setError(null)
    setMetrics(null)
    setAllMetrics(null)
    setProgress(null)
    setTaskId(null)

    try {
      const response = await fetch('/api/train', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model_type: modelType,
          async: true,
          epochs: parseInt(epochs),
          learning_rate: 0.001,
          hidden_sizes: [64, 32, 16],
        }),
      })

      const data = await response.json()

      if (data.success && data.task_id) {
        // Start polling for task status
        setTaskId(data.task_id)
        setProgress({
          current: 0,
          total: 100,
          percent: 0,
          message: 'Task submitted, waiting to start...'
        })

        // Poll every 2 seconds
        pollInterval.current = setInterval(() => {
          pollTaskStatus(data.task_id)
        }, 2000)

        // Initial poll
        pollTaskStatus(data.task_id)
      } else {
        setError(data.message || 'Failed to submit training task')
        setTraining(false)
      }
    } catch (err) {
      setError('Failed to connect to the server. Make sure the backend is running.')
      console.error(err)
      setTraining(false)
    }
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-6">Model Training</h2>
      
      <div className="space-y-4">
        {/* Model Type Selector */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Model Type
          </label>
          <select
            value={modelType}
            onChange={(e) => setModelType(e.target.value)}
            className="input-field"
            disabled={training}
          >
            <option value="tensorflow">TensorFlow</option>
            <option value="pytorch">PyTorch</option>
            <option value="xgboost">XGBoost</option>
            <option value="all">All Models</option>
          </select>
          <p className="text-xs text-gray-500 mt-1">
            Select which model(s) to train
          </p>
        </div>

        {/* Epochs Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Training Epochs
          </label>
          <input
            type="number"
            value={epochs}
            onChange={(e) => setEpochs(e.target.value)}
            className="input-field"
            min="100"
            max="2000"
            step="100"
            disabled={training}
          />
          <p className="text-xs text-gray-500 mt-1">
            More epochs = better accuracy but longer training time
          </p>
        </div>

        {/* Network Architecture Info */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="font-semibold text-sm mb-2">Network Architecture</h3>
          <div className="text-sm text-gray-600 space-y-1">
            <div>• Input: 8 features</div>
            <div>• Hidden: 64 → 32 → 16 neurons</div>
            <div>• Output: 1 (price prediction)</div>
            <div>• Activation: ReLU</div>
            <div>• Learning Rate: 0.001</div>
          </div>
        </div>

        {/* Train Button */}
        <button
          onClick={handleTrain}
          disabled={training}
          className="btn-primary w-full"
        >
          {training ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Training Model...
            </span>
          ) : (
            'Train Model (Async with Celery)'
          )}
        </button>

        {/* Progress Bar */}
        {training && progress && (
          <div className="space-y-2">
            <div className="p-4 bg-blue-50 text-blue-700 rounded-lg">
              <div className="text-sm font-medium mb-2">{progress.message}</div>
              
              {/* Progress Bar */}
              <div className="w-full bg-blue-200 rounded-full h-4 overflow-hidden">
                <div 
                  className="bg-blue-600 h-4 transition-all duration-300 ease-out flex items-center justify-center text-xs text-white font-semibold"
                  style={{ width: `${progress.percent}%` }}
                >
                  {progress.percent > 10 && `${progress.percent}%`}
                </div>
              </div>
              
              {taskId && (
                <div className="text-xs text-blue-600 mt-2 font-mono">
                  Task ID: {taskId}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-6 p-4 bg-red-100 text-red-700 rounded-lg border border-red-300 text-sm">
          {error}
        </div>
      )}

      {/* Training Metrics - Single Model */}
      {metrics && !allMetrics && (
        <div className="mt-6 space-y-4">
          <div className="border-t pt-4">
            <h3 className="font-semibold mb-3 text-green-700">
              ✓ Training Complete!
            </h3>
            
            <div className="space-y-3">
              <div className="bg-green-50 p-3 rounded-lg">
                <div className="text-sm font-medium text-gray-700 mb-1">
                  R² Score (Accuracy)
                </div>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <span className="text-gray-600">Train:</span>
                    <span className="ml-2 font-semibold text-green-700">
                      {(metrics.train_r2 * 100).toFixed(2)}%
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600">Test:</span>
                    <span className="ml-2 font-semibold text-green-700">
                      {(metrics.test_r2 * 100).toFixed(2)}%
                    </span>
                  </div>
                </div>
              </div>

              <div className="bg-blue-50 p-3 rounded-lg">
                <div className="text-sm font-medium text-gray-700 mb-1">
                  RMSE (Error)
                </div>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <span className="text-gray-600">Train:</span>
                    <span className="ml-2 font-semibold text-blue-700">
                      ${(metrics.train_rmse * 100000).toLocaleString('en-US', { maximumFractionDigits: 0 })}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600">Test:</span>
                    <span className="ml-2 font-semibold text-blue-700">
                      ${(metrics.test_rmse * 100000).toLocaleString('en-US', { maximumFractionDigits: 0 })}
                    </span>
                  </div>
                </div>
              </div>

              <div className="text-xs text-gray-500 mt-2">
                Higher R² is better (closer to 100%). Lower RMSE is better.
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Training Metrics - All Models */}
      {allMetrics && (
        <div className="mt-6 space-y-4">
          <div className="border-t pt-4">
            <h3 className="font-semibold mb-3 text-green-700">
              ✓ All Models Training Complete!
            </h3>
            
            {Object.entries(allMetrics).map(([modelName, modelMetrics]) => (
              <div key={modelName} className="mb-4 p-4 bg-gray-50 rounded-lg">
                <h4 className="font-semibold text-sm mb-2 uppercase text-gray-800">
                  {modelName}
                </h4>
                
                <div className="space-y-2">
                  <div className="bg-green-50 p-2 rounded">
                    <div className="text-xs font-medium text-gray-700 mb-1">
                      R² Score
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div>
                        Train: <span className="font-semibold text-green-700">
                          {(modelMetrics.train_r2 * 100).toFixed(2)}%
                        </span>
                      </div>
                      <div>
                        Test: <span className="font-semibold text-green-700">
                          {(modelMetrics.test_r2 * 100).toFixed(2)}%
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-blue-50 p-2 rounded">
                    <div className="text-xs font-medium text-gray-700 mb-1">
                      RMSE
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div>
                        Train: <span className="font-semibold text-blue-700">
                          ${(modelMetrics.train_rmse * 100000).toLocaleString('en-US', { maximumFractionDigits: 0 })}
                        </span>
                      </div>
                      <div>
                        Test: <span className="font-semibold text-blue-700">
                          ${(modelMetrics.test_rmse * 100000).toLocaleString('en-US', { maximumFractionDigits: 0 })}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

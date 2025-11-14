'use client'

import { useState, useEffect } from 'react'

interface ModelCharacteristics {
  name: string
  architecture: string
  layers: string
  parameters: string
  framework: string
  activation: string
  optimizer: string
  strengths: string[]
  best_for: string
  training_speed: string
  inference_speed: string
  typical_use: string
}

interface ModelInfo {
  trained: boolean
  characteristics: ModelCharacteristics
  model_file: string
}

export default function ModelComparison() {
  const [models, setModels] = useState<Record<string, ModelInfo> | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchModelStatus()
  }, [])

  const fetchModelStatus = async () => {
    try {
      const response = await fetch('/api/models/status')
      const data = await response.json()

      if (data.success) {
        setModels(data.models)
      } else {
        setError('Failed to fetch model status')
      }
    } catch (err) {
      setError('Failed to connect to the server')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <h2 className="text-2xl font-bold mb-6">Model Comparison</h2>
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card">
        <h2 className="text-2xl font-bold mb-6">Model Comparison</h2>
        <div className="p-4 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      </div>
    )
  }

  const modelTypes = ['tensorflow', 'pytorch', 'xgboost'] as const

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-6">🔬 Model Architecture Comparison</h2>
      
      <div className="space-y-8">
        {/* Training Status Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {modelTypes.map((modelType) => {
            const model = models?.[modelType]
            const isTrained = model?.trained || false

            return (
              <div key={modelType} className={`p-4 rounded-lg border-2 ${
                isTrained 
                  ? 'bg-green-50 border-green-300' 
                  : 'bg-gray-50 border-gray-300'
              }`}>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-gray-800 uppercase">{modelType}</h3>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    isTrained 
                      ? 'bg-green-600 text-white' 
                      : 'bg-gray-400 text-white'
                  }`}>
                    {isTrained ? '✓ Trained' : 'Not Trained'}
                  </span>
                </div>
                <p className="text-sm text-gray-600">{model?.characteristics?.name || 'Model'}</p>
              </div>
            )
          })}
        </div>

        {/* Detailed Comparison Table */}
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Aspect
                </th>
                {modelTypes.map((modelType) => (
                  <th key={modelType} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {modelType}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Framework
                </td>
                {modelTypes.map((modelType) => (
                  <td key={modelType} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {models?.[modelType]?.characteristics?.framework || 'N/A'}
                  </td>
                ))}
              </tr>

              <tr className="bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Architecture
                </td>
                {modelTypes.map((modelType) => (
                  <td key={modelType} className="px-6 py-4 text-sm text-gray-500">
                    {models?.[modelType]?.characteristics?.architecture || 'N/A'}
                  </td>
                ))}
              </tr>

              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Layer Structure
                </td>
                {modelTypes.map((modelType) => (
                  <td key={modelType} className="px-6 py-4 text-sm text-gray-500 font-mono">
                    {models?.[modelType]?.characteristics?.layers || 'N/A'}
                  </td>
                ))}
              </tr>

              <tr className="bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Parameters
                </td>
                {modelTypes.map((modelType) => (
                  <td key={modelType} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {models?.[modelType]?.characteristics?.parameters || 'N/A'}
                  </td>
                ))}
              </tr>

              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Activation Functions
                </td>
                {modelTypes.map((modelType) => (
                  <td key={modelType} className="px-6 py-4 text-sm text-gray-500">
                    {models?.[modelType]?.characteristics?.activation || 'N/A'}
                  </td>
                ))}
              </tr>

              <tr className="bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Training Speed
                </td>
                {modelTypes.map((modelType) => (
                  <td key={modelType} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {models?.[modelType]?.characteristics?.training_speed || 'N/A'}
                  </td>
                ))}
              </tr>

              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Inference Speed
                </td>
                {modelTypes.map((modelType) => (
                  <td key={modelType} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {models?.[modelType]?.characteristics?.inference_speed || 'N/A'}
                  </td>
                ))}
              </tr>

              <tr className="bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Best For
                </td>
                {modelTypes.map((modelType) => (
                  <td key={modelType} className="px-6 py-4 text-sm text-gray-500">
                    {models?.[modelType]?.characteristics?.best_for || 'N/A'}
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>

        {/* Strengths Comparison */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {modelTypes.map((modelType) => {
            const model = models?.[modelType]
            return (
              <div key={modelType} className="p-4 bg-white border border-gray-200 rounded-lg">
                <h3 className="font-bold text-gray-800 uppercase mb-3">{modelType}</h3>
                <h4 className="text-sm font-semibold text-gray-600 mb-2">Key Strengths:</h4>
                <ul className="space-y-1">
                  {model?.characteristics?.strengths?.map((strength, idx) => (
                    <li key={idx} className="text-sm text-gray-600 flex items-start">
                      <span className="text-green-500 mr-2">✓</span>
                      {strength}
                    </li>
                  )) || <li className="text-sm text-gray-400">No data available</li>}
                </ul>
              </div>
            )
          })}
        </div>

        {/* Usage Recommendations */}
        <div className="p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
          <h3 className="font-bold text-lg text-gray-800 mb-4">💡 When to Use Each Model</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {modelTypes.map((modelType) => {
              const model = models?.[modelType]
              return (
                <div key={modelType} className="p-3 bg-white rounded border border-blue-100">
                  <h4 className="font-semibold text-gray-800 uppercase mb-2">{modelType}</h4>
                  <p className="text-sm text-gray-600">
                    {model?.characteristics?.typical_use || 'General purpose machine learning'}
                  </p>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}


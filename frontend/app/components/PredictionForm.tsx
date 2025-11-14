'use client'

import { useState } from 'react'

interface PredictionFormProps {
  modelTrained: boolean
}

interface FormData {
  sqft: string
  bedrooms: string
  bathrooms: string
  latitude: string
  longitude: string
  median_income: string
  house_age: string
  model_preference: string
  priority: string
}

export default function PredictionForm({ modelTrained }: PredictionFormProps) {
  const [formData, setFormData] = useState<FormData>({
    sqft: '1500',
    bedrooms: '3',
    bathrooms: '2',
    latitude: '34.05',
    longitude: '-118.25',
    median_income: '3.5',
    house_age: '25',
    model_preference: 'auto',
    priority: 'accuracy',
  })

  const [prediction, setPrediction] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [modelUsed, setModelUsed] = useState<string | null>(null)
  const [routingExplanation, setRoutingExplanation] = useState<string | null>(null)
  const [ensemblePredictions, setEnsemblePredictions] = useState<Record<string, number> | null>(null)

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!modelTrained) {
      setError('Please train the model first before making predictions.')
      return
    }

    setLoading(true)
    setError(null)
    setPrediction(null)
    setModelUsed(null)
    setRoutingExplanation(null)
    setEnsemblePredictions(null)

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sqft: parseFloat(formData.sqft),
          bedrooms: parseFloat(formData.bedrooms),
          bathrooms: parseFloat(formData.bathrooms),
          latitude: parseFloat(formData.latitude),
          longitude: parseFloat(formData.longitude),
          median_income: parseFloat(formData.median_income),
          house_age: parseFloat(formData.house_age),
          model_preference: formData.model_preference,
          criteria: { priority: formData.priority },
        }),
      })

      const data = await response.json()

      if (data.success) {
        setPrediction(data.predicted_price)
        setModelUsed(data.model_used)
        setRoutingExplanation(data.routing_explanation)
        setEnsemblePredictions(data.ensemble_predictions || null)
      } else {
        setError(data.message || 'Prediction failed')
      }
    } catch (err) {
      setError('Failed to connect to the server. Make sure the backend is running.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const popularLocations = [
    { name: 'Los Angeles', lat: 34.05, lng: -118.25 },
    { name: 'San Francisco', lat: 37.77, lng: -122.42 },
    { name: 'San Diego', lat: 32.72, lng: -117.16 },
    { name: 'Sacramento', lat: 38.58, lng: -121.49 },
  ]

  const setLocation = (lat: number, lng: number) => {
    setFormData(prev => ({
      ...prev,
      latitude: lat.toString(),
      longitude: lng.toString()
    }))
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-6">Predict House Price</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Model Selection */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-lg border border-blue-200">
          <h3 className="text-lg font-semibold mb-3 text-gray-800">🤖 Model Selection</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Model Preference
              </label>
              <select
                name="model_preference"
                value={formData.model_preference}
                onChange={handleInputChange}
                className="input-field"
              >
                <option value="auto">Auto (LangGraph decides)</option>
                <option value="tensorflow">TensorFlow ANN</option>
                <option value="pytorch">PyTorch ANN</option>
                <option value="xgboost">XGBoost Model</option>
                <option value="ensemble">Ensemble (All 3)</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">
                Choose model or let LangGraph select automatically
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Priority (for Auto mode)
              </label>
              <select
                name="priority"
                value={formData.priority}
                onChange={handleInputChange}
                className="input-field"
                disabled={formData.model_preference !== 'auto'}
              >
                <option value="accuracy">Accuracy</option>
                <option value="speed">Speed</option>
                <option value="experimental">Experimental</option>
                <option value="balanced">Balanced (Ensemble)</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">
                Selection criteria when using Auto mode
              </p>
            </div>
          </div>
        </div>

        {/* Basic Features */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Square Footage
            </label>
            <input
              type="number"
              name="sqft"
              value={formData.sqft}
              onChange={handleInputChange}
              className="input-field"
              min="500"
              max="10000"
              step="100"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Bedrooms
            </label>
            <input
              type="number"
              name="bedrooms"
              value={formData.bedrooms}
              onChange={handleInputChange}
              className="input-field"
              min="1"
              max="10"
              step="1"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Bathrooms
            </label>
            <input
              type="number"
              name="bathrooms"
              value={formData.bathrooms}
              onChange={handleInputChange}
              className="input-field"
              min="1"
              max="10"
              step="0.5"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              House Age (years)
            </label>
            <input
              type="number"
              name="house_age"
              value={formData.house_age}
              onChange={handleInputChange}
              className="input-field"
              min="0"
              max="100"
              step="1"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Median Income (in $10k)
            </label>
            <input
              type="number"
              name="median_income"
              value={formData.median_income}
              onChange={handleInputChange}
              className="input-field"
              min="0.5"
              max="15"
              step="0.1"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              e.g., 3.5 = $35,000 median income
            </p>
          </div>
        </div>

        {/* Location */}
        <div className="border-t pt-6">
          <h3 className="text-lg font-semibold mb-4">Location</h3>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Quick Select:
            </label>
            <div className="flex flex-wrap gap-2">
              {popularLocations.map((loc) => (
                <button
                  key={loc.name}
                  type="button"
                  onClick={() => setLocation(loc.lat, loc.lng)}
                  className="px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                >
                  {loc.name}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Latitude
              </label>
              <input
                type="number"
                name="latitude"
                value={formData.latitude}
                onChange={handleInputChange}
                className="input-field"
                min="32"
                max="42"
                step="0.01"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Longitude
              </label>
              <input
                type="number"
                name="longitude"
                value={formData.longitude}
                onChange={handleInputChange}
                className="input-field"
                min="-125"
                max="-114"
                step="0.01"
                required
              />
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || !modelTrained}
          className="btn-primary w-full"
        >
          {loading ? 'Predicting...' : 'Predict Price'}
        </button>
      </form>

      {/* Error Message */}
      {error && (
        <div className="mt-6 p-4 bg-red-100 text-red-700 rounded-lg border border-red-300">
          {error}
        </div>
      )}

      {/* Prediction Result */}
      {prediction !== null && (
        <div className="mt-6 space-y-4">
          <div className="p-6 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-lg shadow-lg">
            <h3 className="text-lg font-semibold mb-2">Predicted House Price</h3>
            <div className="text-4xl font-bold">
              ${prediction.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </div>
            <p className="mt-2 text-primary-100 text-sm">
              Based on California housing market data
            </p>
          </div>

          {/* Model Info */}
          {modelUsed && (
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-semibold text-gray-700">Model Used:</p>
                  <p className="text-lg font-bold text-blue-700 uppercase">{modelUsed}</p>
                </div>
                {modelUsed === 'ensemble' && (
                  <span className="px-3 py-1 bg-blue-600 text-white text-xs rounded-full">
                    Best Accuracy
                  </span>
                )}
              </div>
              {routingExplanation && (
                <p className="mt-2 text-sm text-gray-600">{routingExplanation}</p>
              )}
            </div>
          )}

          {/* Ensemble Predictions Breakdown */}
          {ensemblePredictions && (
            <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
              <h4 className="text-sm font-semibold text-gray-700 mb-3">Individual Model Predictions:</h4>
              <div className="space-y-2">
                {Object.entries(ensemblePredictions).map(([model, price]) => (
                  <div key={model} className="flex justify-between items-center">
                    <span className="text-sm font-medium text-gray-600 uppercase">{model}:</span>
                    <span className="text-sm font-bold text-gray-800">
                      ${price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}


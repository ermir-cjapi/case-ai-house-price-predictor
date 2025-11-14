'use client'

import { useState, useEffect } from 'react'
import PredictionForm from '@/app/components/PredictionForm'
import TrainingPanel from '@/app/components/TrainingPanel'
import ModelComparison from '@/app/components/ModelComparison'

export default function Home() {
  const [modelTrained, setModelTrained] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if model is trained on mount
    checkModelStatus()
  }, [])

  const checkModelStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/model-info')
      const data = await response.json()
      setModelTrained(data.trained || false)
    } catch (error) {
      console.error('Error checking model status:', error)
      setModelTrained(false)
    } finally {
      setLoading(false)
    }
  }

  const handleTrainingComplete = () => {
    setModelTrained(true)
  }

  return (
    <main className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            House Price Predictor
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            AI-powered house price prediction using multiple neural network frameworks
            (TensorFlow, PyTorch, Transformer) with LangGraph intelligent routing
          </p>
        </div>

        {/* Model Status Banner */}
        {!loading && (
          <div className={`mb-8 p-4 rounded-lg text-center ${
            modelTrained 
              ? 'bg-green-100 text-green-800 border border-green-300'
              : 'bg-yellow-100 text-yellow-800 border border-yellow-300'
          }`}>
            {modelTrained 
              ? '✓ Model is trained and ready for predictions'
              : '⚠ Model not trained yet. Please train the model first.'}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Prediction Form - Takes 2 columns on large screens */}
          <div className="lg:col-span-2">
            <PredictionForm modelTrained={modelTrained} />
          </div>

          {/* Training Panel - Takes 1 column on large screens */}
          <div className="lg:col-span-1">
            <TrainingPanel onTrainingComplete={handleTrainingComplete} />
          </div>
        </div>

        {/* Model Comparison Section */}
        <div className="mt-12">
          <ModelComparison />
        </div>

        {/* Info Section */}
        <div className="mt-12 card">
          <h2 className="text-2xl font-bold mb-4">About This Project</h2>
          <div className="space-y-4 text-gray-600">
            <p>
              This application demonstrates three different neural network implementations 
              for house price prediction, showcasing the flexibility and power of modern ML frameworks:
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 my-6">
              <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <h3 className="font-bold text-blue-900 mb-2">TensorFlow/Keras</h3>
                <p className="text-sm">Industry-standard framework with production-ready features and excellent documentation.</p>
              </div>
              <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                <h3 className="font-bold text-purple-900 mb-2">PyTorch</h3>
                <p className="text-sm">Research-friendly framework with dynamic computation graphs and fast inference.</p>
              </div>
              <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                <h3 className="font-bold text-green-900 mb-2">Transformer</h3>
                <p className="text-sm">State-of-the-art attention-based architecture adapted for tabular data.</p>
              </div>
            </div>
            <p>
              The system uses <strong>LangGraph</strong> for intelligent model routing, 
              automatically selecting the best model based on your preferences (speed, accuracy, experimental) 
              or allowing you to compare all three models side-by-side.
            </p>
            <p>
              All models are trained on the California Housing Dataset, which contains 
              information about houses in California including location, age, rooms, 
              and median income in the area.
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}


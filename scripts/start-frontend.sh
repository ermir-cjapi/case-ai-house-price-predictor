#!/bin/bash

echo "Starting House Price Predictor Frontend..."
echo ""

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
    echo ""
fi

# Start Next.js development server
echo "Starting Next.js development server on port 3000..."
echo ""
npm run dev


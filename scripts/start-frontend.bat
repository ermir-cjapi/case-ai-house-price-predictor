@echo off
echo Starting House Price Predictor Frontend...
echo.

cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
    echo.
)

REM Start Next.js development server
echo Starting Next.js development server on port 3000...
echo.
npm run dev

pause


#!/bin/bash

# Function to stop background processes when you press Ctrl+C
cleanup() {
    echo ""
    echo "🛑 Stopping Bar Gemini servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Execute cleanup function on exit
trap cleanup SIGINT SIGTERM

echo "🚀 Launching Bar Gemini Renovation..."

# 1. Start Backend
echo "📡 Starting Backend (FastAPI) on http://localhost:8000..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
fi
python3 main.py > /dev/null 2>&1 &
BACKEND_PID=$!
cd ..

# 2. Start Frontend
echo "💻 Starting Frontend (Vite) on http://localhost:5173..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✨ Everything is running!"
echo "👉 View Website: http://localhost:5173"
echo "👉 Admin Panel: http://localhost:5173/login"
echo "👉 Press Ctrl+C to stop both servers."

# Keep the script running to catch Ctrl+C
wait

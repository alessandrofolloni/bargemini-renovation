#!/bin/bash

echo "🚀 Starting Bar Gemini Renovation Setup..."

# 1. Setup Backend
echo "📦 Setting up Python Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
# Removing sqlite3 if it exists in requirements.txt (it's built-in)
sed -i '' '/sqlite3/d' requirements.txt 2>/dev/null || sed -i '/sqlite3/d' requirements.txt
pip install -r requirements.txt
echo "✅ Backend dependencies installed."

# 2. Setup Frontend
echo "📦 Setting up Vue.js Frontend..."
cd ../frontend
# Ensure vite.config.js exists
if [ ! -f vite.config.js ]; then
echo "import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
export default defineConfig({
  plugins: [vue()],
})" > vite.config.js
fi
npm install
echo "✅ Frontend dependencies installed."

echo "🎉 Setup complete!"
echo "To run the project:"
echo "1. Terminal 1 (Backend): cd backend && source venv/bin/activate && python main.py"
echo "2. Terminal 2 (Frontend): cd frontend && npm run dev"

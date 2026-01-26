# Bar Gemini Renovation

This project is a modern renovation of the Bar Gemini website, featuring a Python (FastAPI) backend and a Vue.js (Vite) frontend.

## Project Structure
- `/backend`: FastAPI Python application.
- `/frontend`: Vue.js 3 application with Vite.

## Backend (Python)
### Prerequisites
- Python 3.9+
- pip

### Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   python main.py
   ```
The API will be available at `http://localhost:8000`.

## Frontend (Vue.js)
### Prerequisites
- Node.js (Latest LTS recommended)
- npm or yarn

### Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
The website will be available at `http://localhost:5173`.

## Features
- **Premium Design**: Modern "Glassmorphism" UI with cinematic hero section.
- **Dynamic Menu**: Fetches data from the backend API.
- **Responsive**: Mobile-first design optimized for all devices.
- **FastAPI Backend**: Clean and efficient API for data management.

## Additional Settings
- **Image handling**: Do you have specific high-resolution photos of the bar or menu items?
- **Menu Management**: Would you like an admin dashboard to update the menu easily?
- **Booking**: Do you need a table reservation system?

# EV Charging Port Analytics & Optimization Suite

A comprehensive AI-driven solution for electric vehicle charging infrastructure management. This project integrates real-time video analytics, demand forecasting, detailed infrastructure recommendations, and a robust interactive dashboard.

![Dashboard Preview](https://via.placeholder.com/800x400?text=EV+Analytics+Dashboard)

## 🚀 Key Features

### 📹 Real-Time Video Analytics
- **Live Vehicle Detection**: Powered by YOLOv8/v11 for accurate vehicle counting.
- **Unique Vehicle Tracking**: Tracks vehicles across frames to ensure each vehicle is counted only once.
- **Queue Experience Metrics**: Calculates **Queue Length**, **Average Queue Length**, and **Average Dwell Time**.
- **Class-wise Breakdown**: Detailed stats for Cars, Trucks, Buses, and Motorcycles.
- **Processing Controls**: Ability to upload videos, monitor processing progress, and reset data.

### 📊 Interactive Dashboard
- **Real-Time Monitoring**: Live view of processed data and charger status.
- **Traffic Analytics**: Visualizations of vehicle flow, peak times, and occupancy.
- **Charger Status**: Live occupancy monitoring (Available, Occupied, Out of Service).

### 🔮 Advanced Forecasting (Backend)
- **Demand Prediction**: Multi-model ensemble (Prophet, XGBoost, LSTM) for 24h/7d demand forecasting.
- **Peak Detection**: Identifies upcoming high-demand periods.
- **Recommendation Engine**: Actionable insights for infrastructure optimization (e.g., "Add 2 DC Fast Chargers").

---

## 🏗️ Architecture

- **Frontend**: React 18, Vite, Tailwind CSS, Recharts, Lucide Icons.
- **Backend**: FastAPI (Python), OpenCV, Ultralytics YOLO, SQLAlchemy, AsyncPG.
- **Database**: PostgreSQL (with TimescaleDB support) or SQLite (fallback).
- **Communication**: REST API for data, WebSockets for real-time updates.

---

## 📋 Prerequisites

- **Node.js** (v16.0.0 or higher)
- **Python** (v3.8 or higher)
- **PostgreSQL** (Optional, for production DB)

---

## �️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd bi3-ev-charging-port
```

### 2. Backend Setup
The backend handles video processing, database management, and API endpoints.

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/KPI:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Note:** If you encounter issues with `torch` and CUDA, the project is configured to work with CPU-only torch as well.

### 3. Frontend Setup
The frontend provides the user interface.

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

---

## 🚀 Running the Application

### 1. Start the Backend Server
In the `backend` directory (with `venv` activated):

```bash
./run_backend.sh
```
*The backend runs on `http://localhost:8000`.*

### 2. Start the Frontend Development Server
In the `frontend` directory:

```bash
npm run dev
```
*The frontend runs on `http://localhost:3000`.*

---

## � Usage Guide

### 1. Dashboard (`/`)
View high-level metrics, active charger status, and recent alerts.

### 2. Monitoring (`/monitoring`)
**Video Analytics Central:**
- **Upload Video**: Upload CCTV footage (mp4, avi) for analysis.
- **Processing Status**: Watch the progress bar as the AI analyzes the video.
- **Real-Time Metrics**: See live updates for:
    - **Current Queue**: How many cars are currently waiting/visible.
    - **Avg Dwell Time**: How long vehicles stay in the frame (proxy for charging/waiting time).
    - **Unique Count**: Total unique vehicles detected.
- **Detection Results**: View a summary of all processed videos.
- **Reset Data**: Use the trash icon to clear all history and start fresh.

### 3. Analytics (`/analytics`)
Deep dive into historical utilization trends, revenue estimations, and peak hour analysis.

### 4. Predictions (`/predictions`)
View AI-generated forecasts for future demand to plan for peak usage.

---

## 🔧 Configuration

### Environment Variables
**Frontend (`frontend/.env`):**
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
```

**Backend (`backend/.env`):**
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
# If DATABASE_URL is invalid/missing, it falls back to SQLite
```

---

## � Troubleshooting

- **Frontend can't connect to Backend**: Ensure both servers are running. Check that the Frontend is pointing to port `8000` (default).
- **Video Upload Fails**: Ensure the `temp_uploads` directory in `backend/` is writable.
- **CUDA/GPU Errors**: The video processor is configured to use CPU if GPU is unavailable. Ensure `torch` is installed correctly.

---

## 🤝 Contributing
1. Fork the repo.
2. Create a feature branch.
3. Submit a Pull Request.

---

**Built with ❤️ for Smart City Infrastructure**

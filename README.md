# EV Charging Port Analytics & Optimization Suite

A comprehensive AI-driven solution for electric vehicle charging infrastructure. This project integrates advanced demand forecasting, computer vision-based traffic analysis, and real-time dashboard analytics.

![Dashboard Preview](frontend/src/assets/screenshot.png) 
*(Note: Replace with actual screenshot)*

## 🚀 Key Features

### 1. **Live Dashboard**
- Real-time visualization of revenue, utilization, and occupancy.
- **AI Video Analysis**: Upload traffic footage to detect vehicles and analyze queue times automatically.
- Interactive charts and heatmaps for historical data analysis.

### 2. **Demand Prediction**
- Multi-model ensemble (Prophet, XGBoost, LSTM) to forecast charger demand for the next 24-48 hours.
- Peak hour detection to optimize pricing dynamics.

### 3. **Smart Recommendations**
- Actionable insights for infrastructure expansion (e.g., "Add 2 DC Fast Chargers to Zone A").
- ROI and impact analysis for suggested changes.

### 4. **Resilient Backend**
- **Dockerized Architecture**: Fully containerized for consistent deployment.
- **Offline Fallback**: Automatically loads synthetic data if the live database is disconnected.
- **Static Video Serving**: Processed video results are served directly for playback.

---

## 🛠️ Quick Start (Docker)

The easiest way to run the application is using Docker Compose.

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running.

### Steps
1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd bi3-ev-charging-port
    ```

2.  **Start the Application**
    ```bash
    docker-compose up --build
    ```
    *This builds the Frontend (React) and Backend (FastAPI, OpenCV, ML) containers.*

3.  **Access the App**
    *   **Frontend**: [http://localhost:3000](http://localhost:3000)
    *   **Backend API**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

---

## 🏗️ Architecture

### **Frontend** (`/frontend`)
- **Stack**: React 18, Vite, Tailwind CSS.
- **Features**: Real-time WebSockets, Video Upload Widget, Recharts visualization.

### **Backend** (`/backend`)
- **Stack**: Python FastAPI, PostgreSQL (TimescaleDB), OpenCV, Ultralytics YOLOv11.
- **Microservices**:
    - `AnalyticsService`: Aggregates metrics (Revenue, Sessions).
    - `VideoService`: Async processing of traffic footage.
    - `PredictionEngine`: Runs ML models for forecasting.

---

## 📂 Project Structure

```bash
bi3-ev-charging-port/
├── backend/
│   ├── app/
│   │   ├── services/       # Core business logic (Video, Analytics)
│   │   ├── routers/        # API Endpoints
│   │   └── models/         # Pydantic Schemas & DB Models
│   ├── static/             # Processed video storage
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/     # React Widgets (VideoAnalysis, Charts)
│   │   └── pages/          # Main Views (Dashboard, Monitoring)
│   └── Dockerfile
├── docker-compose.yml      # Orchestration config
└── README.md               # Documentation
```

---

## 🔧 Troubleshooting

**1. "Ports already in use" error:**
   - Ensure other services aren't running on ports `3000` or `8000`.
   - Run `docker-compose down` to stop any orphaned containers.

**2. Dashboard is empty (No Data):**
   - The system automatically loads `synthetic_data.csv` if the database is empty or unreachable. Check the backend logs: `docker-compose logs backend`.

**3. Video Upload fails:**
   - Ensure the file is a valid video format (`.mp4`, `.avi`, `.mov`).
   - Check if the backend volume is mounted correctly (persisting data in `/app/static`).

---

## 🔮 Roadmap

- [ ] Interactive India Map integration.
- [ ] User Authentication & Role Management.
- [ ] Mobile App Companion.
- [ ] Direct IP Camera streaming support.

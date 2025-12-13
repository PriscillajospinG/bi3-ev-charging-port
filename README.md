<<<<<<< HEAD
# EV Charging Port Analytics & Optimization Suite

A comprehensive AI-driven solution for electric vehicle charging infrastructure. This project integrates advanced demand forecasting, detailed infrastructure recommendations, and a robust backend logic layer for analytics dashboards.

## 🚀 Key Modules

### 1. Demand Prediction Engine (`backend/models/prediction/`)
Accurate demand forecasting using a multi-model ensemble approach.
- **Models**: Prophet (Trend), XGBoost (Events), LSTM (Sequences).
- **Features**: 24h/7d forecasts, peak detection, confidence intervals, and MAPE accuracy evaluation.

### 2. Recommendation Engine (`backend/models/recommendations/`)
Actionable insights for infrastructure optimization.
- **Logic**: Rule-based analysis of utilization, queues, and revenue.
- **Outputs**: Prioritized recommendations (e.g., "Add Charger", "Optimize Layout") with ROI and confidence scores.

### 3. Analytics Backend Layer (`backend/models/analytics/`)
The core logic powering the user-facing Analytics Dashboard.
- **Metrics**: Real-time calculation of Utilization, Sessions, Energy, and Revenue (with % change).
- **Forecasting**: Internal ensemble model for dashboard predictions.
- **Structure**: Generates the exact JSON schema required by the UI.

### 4. Backend Dashboard Engine (`backend/models/dashboard/`)
Comprehensive analytics engine for the real-time dashboard.
- **Components**: Revenue, Occupancy, Traffic, Alerts, Performance, Forecast.
- **Output**: Unified JSON structure `dashboard_data.json` for frontend consumption.
- **Features**: Real-time status simulation, Prophet-based alerts, and charger-level metrics.

---

## 📂 Directory Structure

```
bi3-ev-charging-port/
├── backend/
│   ├── models/
│   │   ├── prediction/             # Standalone Demand Prediction
│   │   │   ├── demand_prediction_engine.py
│   │   │   └── run.sh
│   │   │
│   │   ├── recommendations/        # Recommendation Engine
│   │   │   ├── recommendation_engine.py
│   │   │   └── recommendations.json
│   │   │
│   │   └── analytics/              # Dashboard Backend Logic
│   │       ├── analytics_backend.py
│   │       ├── analytics_dashboard.json
│   │       └── run_with_libomp.sh
│
└── README.md                   # Project Documentation
```

---

## 🛠️ Usage Guide

### A. Run Demand Prediction
```bash
cd backend/models/prediction
./run.sh
```
**Output:** `forecast_result.json`, `forecast_plot.png`

### B. Run Recommendations
```bash
cd backend/models/recommendations
python3 -m venv venv && ./venv/bin/pip install -r requirements.txt
./venv/bin/python recommendation_engine.py
```
**Output:** `recommendations.json` (Includes confidence accuracy scores)

### C. Run Analytics Backend
```bash
cd backend/models/analytics
./run_with_libomp.sh
```
**Output:** 
- `analytics_dashboard.json`: Complete dashboard data.
- `forecast_result.json`: Backend internal forecast check.

---

## 📊 Sample Data

**Dashboard Structure (`analytics_dashboard.json`):**
```json
{
  "summary": {
    "avg_utilization": "74.2%",
    "revenue": "$3,847",
    "revenue_change": "+8.7%"
  },
  "daily_trend": [ ... ],
  "status_distribution": { "available": { "percent": 52 } }
}
```
=======
# EV Charging Port Analytics Dashboard

A comprehensive React-based business intelligence dashboard for EV charging port operations, powered by NVIDIA DeepStream and AI-driven analytics.

## 🚀 Features

### Real-Time Monitoring
- **Live Camera Feeds**: Multi-camera support with RTSP/CSI/USB streams
- **Object Detection**: YOLOv8/YOLOv11/RT-DETR powered vehicle and charger detection
- **Traffic Analytics**: Real-time queue detection, dwell time tracking, and vehicle counting
- **Charger Status**: Live occupancy monitoring and session tracking

### Advanced Analytics
- **Utilization Charts**: Time-series visualization of charger usage patterns
- **Heat Maps**: Weekly utilization patterns across different time periods
- **Performance Metrics**: Detailed charger-level statistics and KPIs
- **Traffic Patterns**: Historical analysis and trend identification

### Demand Prediction
- **AI Forecasting**: LSTM/Prophet/XGBoost models for demand prediction
- **Peak Detection**: Identify upcoming high-demand periods
- **Seasonal Analysis**: Event-based and seasonal pattern recognition
- **Confidence Scoring**: Prediction accuracy and confidence intervals

### Smart Recommendations
- **Infrastructure Optimization**: Add/remove/relocate charger suggestions
- **ROI Analysis**: Cost-benefit analysis for each recommendation
- **Priority Ranking**: High/medium/low priority classification
- **Impact Assessment**: Expected utilization and revenue improvements

## 🏗️ Architecture

### DeepStream Pipeline
```
Camera Inputs → nvv4l2decoder → nvstreammux → nvdspreprocess
                                                    ↓
                                                nvinfer (YOLO)
                                                    ↓
                                                nvtracker
                                                    ↓
                                            Analytics Layer
                                                    ↓
                                        Prediction Engine (LSTM)
                                                    ↓
                                        Recommendation Engine
                                                    ↓
                                            Dashboard (React)
```

### Frontend Stack
- **Framework**: React 18 with Vite
- **Routing**: React Router v6
- **State Management**: Zustand
- **Charts**: Recharts
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **API Client**: Axios
- **WebSocket**: Native WebSocket API

## 📦 Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd bi3-ev-charging-port
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your backend API endpoints
```

4. **Start development server**
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws

# Feature Flags
VITE_ENABLE_MOCK_DATA=true
VITE_ENABLE_WEBSOCKET=true
```

### Backend Integration

The frontend expects the following backend endpoints:

- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/chargers` - List all chargers
- `GET /api/analytics/utilization` - Utilization data
- `GET /api/predictions/demand` - Demand forecast
- `GET /api/recommendations` - AI recommendations
- `WS /ws` - WebSocket for real-time updates

## 🎨 Project Structure

```
src/
├── components/          # React components
│   ├── Analytics/       # Charts and analytics components
│   ├── Layout/          # Layout components (Header, Sidebar)
│   ├── Monitoring/      # Real-time monitoring components
│   ├── Predictions/     # Prediction and forecast components
│   └── Recommendations/ # Recommendation components
├── pages/               # Page components
│   ├── Dashboard.jsx
│   ├── Analytics.jsx
│   ├── Monitoring.jsx
│   ├── Predictions.jsx
│   └── Recommendations.jsx
├── services/            # API and WebSocket services
│   ├── api.js
│   └── websocket.js
├── store/               # Zustand state management
│   └── useAppStore.js
├── hooks/               # Custom React hooks
│   └── index.js
├── utils/               # Utility functions
│   └── helpers.js
├── App.jsx              # Main application component
├── main.jsx             # Application entry point
└── index.css            # Global styles
```

## 🛠️ Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 📊 Features by Page

### Dashboard (`/`)
- Real-time traffic statistics
- Quick charger status overview
- Utilization trends
- Occupancy distribution
- Quick action cards

### Analytics (`/analytics`)
- Detailed utilization charts (line, bar, area)
- Weekly heatmaps
- Performance metrics
- Charger-level statistics table
- Export functionality

### Live Monitoring (`/monitoring`)
- 4+ camera feed displays
- Real-time object detection overlays
- Live charger status cards
- Detection pipeline metrics
- Traffic flow visualization

### Predictions (`/predictions`)
- 24-48 hour demand forecast
- Peak time predictions
- Seasonal pattern analysis
- Model accuracy metrics
- Confidence intervals

### Recommendations (`/recommendations`)
- Infrastructure optimization suggestions
- Priority-based filtering
- ROI and cost analysis
- Implementation impact assessment
- Data-driven insights

## 🔌 WebSocket Events

The application subscribes to the following WebSocket events:

- `metrics_update` - Real-time metrics updates
- `charger_update` - Charger status changes
- `traffic_update` - Traffic flow updates
- `camera_feed` - Camera feed updates
- `alert` - System alerts and notifications

## 🎯 Mock Data

For development without a backend, the application includes comprehensive mock data:

- Charger status and metrics
- Historical utilization data
- Traffic statistics
- Demand forecasts
- Recommendations

Enable mock data in `.env`:
```env
VITE_ENABLE_MOCK_DATA=true
```

## 🚢 Deployment

### Build for production
```bash
npm run build
```

The build output will be in the `dist/` directory.

### Deploy to static hosting
```bash
# Example: Deploy to Netlify
netlify deploy --prod --dir=dist

# Example: Deploy to Vercel
vercel --prod
```

## 🔐 Security Considerations

- All API calls use HTTPS in production
- WebSocket connections are secured with WSS
- Authentication tokens stored in localStorage
- CORS configured for allowed origins
- Input validation on all user inputs

## 📈 Performance

- Code splitting for optimal load times
- Lazy loading for route components
- Optimized bundle size with tree shaking
- Responsive images and assets
- Efficient re-rendering with React.memo

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is proprietary software for EV charging port analytics.

## 🆘 Support

For issues and questions:
- Create an issue in the repository
- Contact the development team
- Check documentation in `/docs`

## 🔮 Roadmap

- [ ] Mobile app companion
- [ ] Advanced ML model integration
- [ ] Multi-site management
- [ ] Custom alert rules
- [ ] Report generation and scheduling
- [ ] Integration with payment systems
- [ ] User role management
- [ ] Historical data export

---

Built with ⚡ for intelligent EV charging infrastructure management
>>>>>>> origin/frontend_env_ws/fix

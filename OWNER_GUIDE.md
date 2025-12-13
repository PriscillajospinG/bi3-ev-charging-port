# EV Charging Port Analytics Dashboard

> **Business Intelligence Platform for Charging Station Owners**  
> Real-time monitoring, revenue tracking, and AI-powered optimization recommendations

## 🎯 Key Features for Station Owners

### 1. **Live Occupancy Monitoring**
- Real-time charger availability display
- Visual occupancy percentage with status indicators
- Queue detection and wait time tracking
- Critical/warning alerts when capacity reaches 75%+
- Instant view of available vs occupied chargers

### 2. **Incoming Traffic Analysis**
- Track vehicles approaching your station
- Estimated arrival times (ETA) for incoming EVs
- Route-based traffic breakdown
- Visual map showing vehicle positions
- Proactive capacity planning

### 3. **Revenue Impact Dashboard**
- **Today's Revenue**: Real-time earnings with daily comparison
- **Weekly Revenue**: 7-day trends and daily averages
- **Monthly Revenue**: Progress toward monthly targets
- **30-Day Projection**: AI-powered revenue forecasting
- Per-charger revenue breakdown

### 4. **Charger Performance & Utilization**
- Individual charger performance scores
- 24-hour session counts per charger
- Revenue generation by charger
- Average session duration tracking
- Utilization rates with visual indicators
- Performance alerts for underperforming units

### 5. **Demand Prediction Engine**
- **Peak hour forecasting**: Know when to expect high demand
- **Seasonal patterns**: Weekly and monthly trend analysis
- **Event-based predictions**: Special event impact forecasting
- **Confidence scoring**: 70-90% accuracy predictions
- **Multi-model ensemble**: LSTM + Prophet + XGBoost

### 6. **Smart Deployment Recommendations**
- **Add Chargers**: High-ROI expansion opportunities
- **Relocate Units**: Move underutilized chargers to high-demand zones
- **Mobile Unit Deployment**: Flexible capacity for peak periods
- **Remove/Decommission**: Identify consistently underperforming chargers
- **Cost-benefit analysis**: ROI timeline for each recommendation
- **Priority ranking**: High/Medium/Low based on impact

### 7. **Critical Alerts System**
- **🔴 Critical Alerts**: High queue, capacity issues, system failures
- **⚠️ Warning Alerts**: Charger downtime, maintenance needed, prolonged sessions
- **ℹ️ Info Alerts**: Peak predictions, routine notifications
- **Misuse Detection**: Vehicles overstaying after charge completion
- **Queue Alerts**: Automated notifications when wait times exceed thresholds
- **Downtime Tracking**: Immediate alerts for offline chargers

---

## 📊 Dashboard Overview

### Main Dashboard (`/`)
**At-a-glance view of your charging business:**

1. **Revenue Metrics** (Top Priority)
   - Today's earnings with % change
   - Weekly and monthly revenue
   - 30-day projections

2. **Live Occupancy**
   - Circular gauge showing % capacity
   - Real-time available/occupied counts
   - Queue length and wait times

3. **Incoming Traffic**
   - Vehicles approaching your station
   - Route analysis and ETAs
   - Visual map display

4. **Active Alerts**
   - Critical issues requiring immediate attention
   - Misuse, downtime, and queue warnings
   - Actionable recommendations

5. **Performance Table**
   - All chargers at a glance
   - Status, utilization, revenue per unit
   - Performance scoring

### Analytics Page (`/analytics`)
- Detailed utilization charts (hourly, daily, weekly)
- Heat maps showing peak usage patterns
- Charger-level performance breakdowns
- Revenue trends and forecasts
- Export functionality for reports

### Live Monitoring (`/monitoring`)
- Real-time camera feeds (4+ cameras)
- Object detection overlays (vehicles, chargers)
- DeepStream pipeline metrics
- Traffic flow visualization
- Live charger status cards

### Predictions (`/predictions`)
- 24-48 hour demand forecasts
- Peak time predictions with confidence scores
- Seasonal pattern recognition
- Event-based demand analysis
- Model accuracy tracking (87%+ typical)

### Recommendations (`/recommendations`)
- AI-generated optimization strategies
- Infrastructure expansion plans
- Cost and ROI analysis
- Priority-based filtering
- Implementation impact assessment

---

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone <repository-url>
cd bi3-ev-charging-port

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Start development server
npm run dev
```

Access dashboard at: `http://localhost:3000`

### Environment Configuration
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
VITE_ENABLE_MOCK_DATA=true
VITE_ENABLE_WEBSOCKET=true
```

---

## 🏗️ Technical Architecture

### DeepStream AI Pipeline
```
📹 Camera Inputs (RTSP/CSI/USB)
    ↓
🎬 nvv4l2decoder (Hardware H.264/H.265 decoding)
    ↓
🔀 nvstreammux (Multi-camera batching)
    ↓
✂️ nvdspreprocess (ROI cropping, normalization)
    ↓
🤖 nvinfer (YOLOv8/v11/RT-DETR object detection)
    ↓
🎯 nvtracker (ByteTrack multi-object tracking)
    ↓
📊 Analytics Layer (Traffic, occupancy, dwell time)
    ↓
🔮 Prediction Engine (LSTM/Prophet/XGBoost)
    ↓
💡 Recommendation Engine
    ↓
📱 React Dashboard (Real-time visualization)
```

### Frontend Technology Stack
- **Framework**: React 18 + Vite (fast dev server)
- **State Management**: Zustand (lightweight, performant)
- **Charts**: Recharts (responsive, customizable)
- **Styling**: Tailwind CSS (utility-first)
- **Icons**: Lucide React (modern icon library)
- **API Client**: Axios (HTTP requests)
- **WebSocket**: Native WebSocket API (real-time updates)
- **Routing**: React Router v6

---

## 📈 Business Value

### ROI Tracking
- **Revenue Visibility**: Track earnings by day/week/month/charger
- **Utilization Optimization**: Identify peak times and underutilized assets
- **Predictive Capacity**: Avoid lost revenue from queue abandonment
- **Maintenance Efficiency**: Proactive alerts reduce downtime costs

### Operational Efficiency
- **Remote Monitoring**: Check status from anywhere
- **Automated Alerts**: No manual checking required
- **Data-Driven Decisions**: AI recommendations backed by analytics
- **Traffic Forecasting**: Staff and prepare for peak periods

### Customer Experience
- **Reduced Wait Times**: Better capacity management
- **Availability Tracking**: Real-time status for customers
- **Misuse Prevention**: Automated overstay notifications
- **Consistent Service**: Performance monitoring ensures reliability

---

## 🔌 API Integration

### Backend Endpoints Required
```javascript
// Dashboard & Metrics
GET  /api/dashboard/stats
GET  /api/metrics/current

// Chargers
GET  /api/chargers
GET  /api/chargers/:id
GET  /api/chargers/status

// Analytics
GET  /api/analytics/utilization?range=24h
GET  /api/analytics/traffic
GET  /api/analytics/heatmap
GET  /api/analytics/occupancy

// Predictions
GET  /api/predictions/demand
GET  /api/predictions/peaks

// Recommendations
GET  /api/recommendations
POST /api/recommendations/:id/implement

// Real-time WebSocket
WS   /ws
```

### WebSocket Events
```javascript
// Subscribe to real-time updates
ws.send({ type: 'subscribe', stream: 'metrics' })
ws.send({ type: 'subscribe', stream: 'charger_status' })
ws.send({ type: 'subscribe', stream: 'traffic' })

// Receive updates
- metrics_update
- charger_update  
- traffic_update
- alert
```

---

## 🛠️ Development

### Project Structure
```
src/
├── components/
│   ├── Dashboard/       # Owner-focused components
│   │   ├── LiveOccupancy.jsx
│   │   ├── RevenueMetrics.jsx
│   │   ├── TrafficFlowMap.jsx
│   │   ├── AlertsPanel.jsx
│   │   └── ChargerPerformanceTable.jsx
│   ├── Analytics/       # Charts and visualizations
│   ├── Monitoring/      # Real-time monitoring
│   ├── Predictions/     # Forecasting components
│   └── Recommendations/ # AI suggestions
├── pages/              # Main views
├── services/           # API & WebSocket
├── store/              # State management
├── hooks/              # Custom React hooks
└── utils/              # Helper functions
```

### Available Scripts
```bash
npm run dev      # Development server
npm run build    # Production build
npm run preview  # Preview production build
npm run lint     # Code linting
```

---

## 📊 Mock Data Mode

For demonstration without backend:

```env
VITE_ENABLE_MOCK_DATA=true
```

Includes realistic data for:
- 6 chargers across 3 zones
- Revenue metrics and trends
- Traffic patterns
- Demand predictions
- Active alerts
- Performance scores

---

## 🚢 Deployment

### Production Build
```bash
npm run build
# Output: dist/ directory
```

### Deploy Options
```bash
# Netlify
netlify deploy --prod --dir=dist

# Vercel
vercel --prod

# AWS S3 + CloudFront
aws s3 sync dist/ s3://your-bucket
```

---

## 🔐 Security

- HTTPS/WSS in production
- JWT token authentication
- localStorage for token persistence
- CORS configuration
- Input validation
- Rate limiting (backend)

---

## 📱 Mobile Responsive

Fully responsive design optimized for:
- Desktop (1920x1080+)
- Laptop (1366x768+)
- Tablet (768x1024)
- Mobile (375x667+)

---

## 🆘 Support & Documentation

- **Issues**: Submit via GitHub Issues
- **Email**: support@ev-charging-analytics.com
- **Docs**: `/docs` directory
- **API Docs**: `/api/docs` (Swagger)

---

## 🗺️ Roadmap

### Phase 2
- [ ] Mobile app (React Native)
- [ ] SMS/Email alert notifications
- [ ] Custom alert rule builder
- [ ] Advanced reporting (PDF generation)
- [ ] Multi-site management

### Phase 3
- [ ] Customer-facing mobile app
- [ ] Payment integration
- [ ] Reservation system
- [ ] Dynamic pricing engine
- [ ] Fleet management features

### Phase 4
- [ ] White-label solution
- [ ] API marketplace
- [ ] Third-party integrations
- [ ] Advanced ML models
- [ ] Blockchain-based billing

---

## 📄 License

Proprietary - All rights reserved

---

**Built with ⚡ for intelligent EV charging infrastructure**  
*Powered by NVIDIA DeepStream + React*
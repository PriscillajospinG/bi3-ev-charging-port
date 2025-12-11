import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout/Layout'
import Dashboard from './pages/Dashboard'
import Analytics from './pages/Analytics'
import Monitoring from './pages/Monitoring'
import Predictions from './pages/Predictions'
import Recommendations from './pages/Recommendations'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/monitoring" element={<Monitoring />} />
          <Route path="/predictions" element={<Predictions />} />
          <Route path="/recommendations" element={<Recommendations />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App

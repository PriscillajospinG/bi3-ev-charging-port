import { Bell, Settings, User } from 'lucide-react'
import { useState } from 'react'

const Header = () => {
  const [notifications] = useState(3)

  return (
    <header className="bg-slate-900 border-b border-slate-800 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <h2 className="text-xl font-semibold text-white">
            EV Charging Port Intelligence
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Real-time analytics and demand forecasting
          </p>
        </div>

        <div className="flex items-center gap-4">
          {/* Notifications */}
          <button className="relative p-2 text-slate-400 hover:text-white transition-colors">
            <Bell size={20} />
            {notifications > 0 && (
              <span className="absolute top-0 right-0 w-5 h-5 bg-danger text-white text-xs rounded-full flex items-center justify-center">
                {notifications}
              </span>
            )}
          </button>

          {/* Settings */}
          <button className="p-2 text-slate-400 hover:text-white transition-colors">
            <Settings size={20} />
          </button>

          {/* User Profile */}
          <button className="flex items-center gap-2 px-3 py-2 bg-slate-800 rounded-lg hover:bg-slate-700 transition-colors">
            <User size={20} />
            <span className="text-sm font-medium">Operator</span>
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header

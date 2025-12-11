import { useEffect, useRef, useState } from 'react'
import { Play, Pause, Maximize2 } from 'lucide-react'

const CameraFeed = ({ cameraId, title, rtspUrl, type = 'road' }) => {
  const videoRef = useRef(null)
  const [isPlaying, setIsPlaying] = useState(true)
  const [isFullscreen, setIsFullscreen] = useState(false)

  useEffect(() => {
    // In production, this would connect to the RTSP stream via WebRTC or HLS
    // For now, we'll use a placeholder
    if (videoRef.current && isPlaying) {
      // videoRef.current.play()
    }
  }, [isPlaying])

  const togglePlay = () => {
    setIsPlaying(!isPlaying)
  }

  const toggleFullscreen = () => {
    if (!isFullscreen) {
      videoRef.current?.requestFullscreen()
    } else {
      document.exitFullscreen()
    }
    setIsFullscreen(!isFullscreen)
  }

  return (
    <div className="card relative">
      <div className="flex items-center justify-between mb-3">
        <div>
          <h3 className="text-lg font-semibold">{title}</h3>
          <p className="text-xs text-slate-400">Camera {cameraId}</p>
        </div>
        <div className={`px-2 py-1 rounded text-xs font-medium ${
          type === 'road' ? 'bg-blue-500/20 text-blue-400' : 'bg-green-500/20 text-green-400'
        }`}>
          {type === 'road' ? 'Road Facing' : 'Charger Facing'}
        </div>
      </div>

      <div className="relative bg-slate-900 rounded-lg overflow-hidden aspect-video">
        <video
          ref={videoRef}
          className="w-full h-full object-cover"
          poster="/placeholder-camera.jpg"
        >
          {/* In production, this would be HLS or WebRTC stream */}
          <source src={rtspUrl} type="video/mp4" />
        </video>

        {/* Overlay with detected objects */}
        <div className="absolute top-2 left-2 space-y-1">
          <div className="bg-black/60 backdrop-blur-sm px-2 py-1 rounded text-xs">
            🚗 Vehicles: <span className="font-semibold text-primary-400">4</span>
          </div>
          <div className="bg-black/60 backdrop-blur-sm px-2 py-1 rounded text-xs">
            ⚡ Chargers: <span className="font-semibold text-success">2/3</span>
          </div>
        </div>

        {/* Live indicator */}
        <div className="absolute top-2 right-2">
          <div className="flex items-center gap-1 bg-danger/80 backdrop-blur-sm px-2 py-1 rounded">
            <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
            <span className="text-xs font-semibold">LIVE</span>
          </div>
        </div>

        {/* Controls */}
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-3">
          <div className="flex items-center justify-between">
            <button
              onClick={togglePlay}
              className="p-2 hover:bg-white/20 rounded transition-colors"
            >
              {isPlaying ? <Pause size={20} /> : <Play size={20} />}
            </button>
            <button
              onClick={toggleFullscreen}
              className="p-2 hover:bg-white/20 rounded transition-colors"
            >
              <Maximize2 size={20} />
            </button>
          </div>
        </div>
      </div>

      <div className="mt-3 text-xs text-slate-500">
        Stream: {rtspUrl || 'Connecting...'}
      </div>
    </div>
  )
}

export default CameraFeed

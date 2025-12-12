import { useState, useEffect } from 'react'
import {
    Car,
    Truck,
    Bus,
    Bike,
    Activity,
    RefreshCw,
    BarChart3,
    Clock,
    CheckCircle,
    AlertCircle,
    Loader,
    ChevronDown,
    ChevronUp
} from 'lucide-react'
import { api } from '../../services/api'

const DetectionResults = () => {
    const [results, setResults] = useState(null)
    const [processingJobs, setProcessingJobs] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [expandedVideo, setExpandedVideo] = useState(null)
    const [autoRefresh, setAutoRefresh] = useState(true)

    const fetchData = async () => {
        try {
            const [resultsRes, statusRes] = await Promise.all([
                api.getVideoResults(),
                api.getAllVideoStatus()
            ])
            setResults(resultsRes.data)
            setProcessingJobs(statusRes.data.jobs || [])
            setError(null)
        } catch (e) {
            console.error('Failed to fetch detection results', e)
            setError('Failed to load detection results')
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchData()

        // Auto-refresh every 5 seconds if enabled
        let interval
        if (autoRefresh) {
            interval = setInterval(fetchData, 5000)
        }
        return () => clearInterval(interval)
    }, [autoRefresh])

    const getVehicleIcon = (className) => {
        switch (className?.toLowerCase()) {
            case 'car': return <Car size={20} className="text-blue-400" />
            case 'truck': return <Truck size={20} className="text-amber-400" />
            case 'bus': return <Bus size={20} className="text-green-400" />
            case 'motorcycle': return <Bike size={20} className="text-purple-400" />
            default: return <Car size={20} className="text-slate-400" />
        }
    }

    const getStatusIcon = (status) => {
        switch (status) {
            case 'completed': return <CheckCircle size={16} className="text-green-400" />
            case 'processing': return <Loader size={16} className="text-blue-400 animate-spin" />
            case 'failed': return <AlertCircle size={16} className="text-red-400" />
            case 'pending': return <Clock size={16} className="text-amber-400" />
            default: return <Clock size={16} className="text-slate-400" />
        }
    }

    const getStatusColor = (status) => {
        switch (status) {
            case 'completed': return 'bg-green-500/20 text-green-400 border-green-500/30'
            case 'processing': return 'bg-blue-500/20 text-blue-400 border-blue-500/30'
            case 'failed': return 'bg-red-500/20 text-red-400 border-red-500/30'
            case 'pending': return 'bg-amber-500/20 text-amber-400 border-amber-500/30'
            default: return 'bg-slate-500/20 text-slate-400 border-slate-500/30'
        }
    }

    if (loading) {
        return (
            <div className="card bg-slate-800/50 border border-slate-700">
                <div className="flex items-center justify-center py-12">
                    <Loader className="animate-spin text-primary-400 mr-3" size={24} />
                    <span className="text-slate-300">Loading detection results...</span>
                </div>
            </div>
        )
    }

    const totalDetections = results?.total_detections || 0
    const videoSummaries = results?.video_summaries || {}
    const hasActiveJobs = processingJobs.some(j => j.status === 'processing')

    return (
        <div className="space-y-6">
            {/* Processing Jobs Status */}
            {processingJobs.length > 0 && (
                <div className="card bg-slate-800/50 border border-slate-700">
                    <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                            <Activity size={24} className="text-primary-400" />
                            <h2 className="text-xl font-semibold">Processing Jobs</h2>
                            {hasActiveJobs && (
                                <span className="px-2 py-1 bg-blue-500/20 text-blue-400 text-xs rounded-full animate-pulse">
                                    Active
                                </span>
                            )}
                        </div>
                        <button
                            onClick={() => setAutoRefresh(!autoRefresh)}
                            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm transition-colors ${autoRefresh
                                    ? 'bg-primary-600 text-white'
                                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                                }`}
                        >
                            <RefreshCw size={14} className={autoRefresh ? 'animate-spin' : ''} />
                            Auto-refresh {autoRefresh ? 'ON' : 'OFF'}
                        </button>
                    </div>

                    <div className="space-y-3">
                        {processingJobs.map((job) => (
                            <div
                                key={job.filename}
                                className={`p-4 rounded-lg border ${getStatusColor(job.status)}`}
                            >
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-3">
                                        {getStatusIcon(job.status)}
                                        <div>
                                            <p className="font-medium">{job.filename}</p>
                                            <p className="text-xs opacity-75">
                                                Status: {job.status}
                                                {job.processed_frames > 0 && ` • Frames: ${job.processed_frames}/${job.total_frames || '?'}`}
                                                {job.detections_count > 0 && ` • Detections: ${job.detections_count}`}
                                            </p>
                                        </div>
                                    </div>
                                    {job.status === 'completed' && job.detection_summary && (
                                        <div className="flex gap-4">
                                            {Object.entries(job.detection_summary).map(([cls, count]) => (
                                                <div key={cls} className="flex items-center gap-1 text-sm">
                                                    {getVehicleIcon(cls)}
                                                    <span>{count}</span>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                                {job.status === 'processing' && job.total_frames > 0 && (
                                    <div className="mt-3">
                                        <div className="w-full bg-slate-700 rounded-full h-2">
                                            <div
                                                className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                                                style={{
                                                    width: `${Math.min(100, (job.processed_frames / (job.total_frames / 30)) * 100)}%`
                                                }}
                                            />
                                        </div>
                                    </div>
                                )}
                                {job.error && (
                                    <p className="mt-2 text-xs text-red-400">Error: {job.error}</p>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Detection Results Summary */}
            <div className="card bg-slate-800/50 border border-slate-700">
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                        <BarChart3 size={24} className="text-primary-400" />
                        <h2 className="text-xl font-semibold">Detection Results</h2>
                    </div>
                    <button
                        onClick={fetchData}
                        className="p-2 rounded-lg bg-slate-700 hover:bg-slate-600 transition-colors"
                    >
                        <RefreshCw size={18} />
                    </button>
                </div>

                {error ? (
                    <div className="text-center py-8 text-red-400">
                        <AlertCircle size={48} className="mx-auto mb-2 opacity-50" />
                        <p>{error}</p>
                    </div>
                ) : totalDetections === 0 ? (
                    <div className="text-center py-12 text-slate-400">
                        <Car size={48} className="mx-auto mb-3 opacity-30" />
                        <p className="text-lg font-medium">No detections yet</p>
                        <p className="text-sm mt-1">Upload a video to start detecting vehicles</p>
                    </div>
                ) : (
                    <div className="space-y-4">
                        {/* Overall Stats */}
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                            <div className="bg-slate-700/50 rounded-lg p-4 text-center">
                                <p className="text-3xl font-bold text-primary-400">{totalDetections}</p>
                                <p className="text-sm text-slate-400">Total Detections</p>
                            </div>
                            <div className="bg-slate-700/50 rounded-lg p-4 text-center">
                                <p className="text-3xl font-bold text-blue-400">{Object.keys(videoSummaries).length}</p>
                                <p className="text-sm text-slate-400">Videos Processed</p>
                            </div>
                            <div className="bg-slate-700/50 rounded-lg p-4 text-center">
                                <div className="flex items-center justify-center gap-2">
                                    <Car size={28} className="text-blue-400" />
                                    <span className="text-3xl font-bold">
                                        {Object.values(videoSummaries).reduce((sum, v) => sum + (v.by_class?.car || 0), 0)}
                                    </span>
                                </div>
                                <p className="text-sm text-slate-400">Cars</p>
                            </div>
                            <div className="bg-slate-700/50 rounded-lg p-4 text-center">
                                <div className="flex items-center justify-center gap-2">
                                    <Truck size={28} className="text-amber-400" />
                                    <span className="text-3xl font-bold">
                                        {Object.values(videoSummaries).reduce((sum, v) => sum + (v.by_class?.truck || 0), 0)}
                                    </span>
                                </div>
                                <p className="text-sm text-slate-400">Trucks</p>
                            </div>
                        </div>

                        {/* Per-Video Breakdown */}
                        <h3 className="text-lg font-semibold text-slate-200 mb-3">By Video</h3>
                        <div className="space-y-2">
                            {Object.entries(videoSummaries).map(([videoSource, data]) => (
                                <div key={videoSource} className="border border-slate-600 rounded-lg overflow-hidden">
                                    <button
                                        onClick={() => setExpandedVideo(expandedVideo === videoSource ? null : videoSource)}
                                        className="w-full flex items-center justify-between p-4 bg-slate-700/30 hover:bg-slate-700/50 transition-colors"
                                    >
                                        <div className="flex items-center gap-3">
                                            <div className="w-10 h-10 bg-slate-600 rounded-lg flex items-center justify-center">
                                                <Activity size={20} className="text-primary-400" />
                                            </div>
                                            <div className="text-left">
                                                <p className="font-medium text-slate-200">{videoSource}</p>
                                                <p className="text-sm text-slate-400">{data.total} detections</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <div className="flex gap-3">
                                                {Object.entries(data.by_class || {}).map(([cls, count]) => (
                                                    <div key={cls} className="flex items-center gap-1">
                                                        {getVehicleIcon(cls)}
                                                        <span className="text-sm text-slate-300">{count}</span>
                                                    </div>
                                                ))}
                                            </div>
                                            {expandedVideo === videoSource ? (
                                                <ChevronUp size={20} className="text-slate-400" />
                                            ) : (
                                                <ChevronDown size={20} className="text-slate-400" />
                                            )}
                                        </div>
                                    </button>

                                    {expandedVideo === videoSource && (
                                        <div className="p-4 bg-slate-800/50 border-t border-slate-600">
                                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                                {Object.entries(data.by_class || {}).map(([cls, count]) => (
                                                    <div
                                                        key={cls}
                                                        className="bg-slate-700/50 rounded-lg p-3 flex items-center gap-3"
                                                    >
                                                        <div className="w-10 h-10 bg-slate-600 rounded-lg flex items-center justify-center">
                                                            {getVehicleIcon(cls)}
                                                        </div>
                                                        <div>
                                                            <p className="text-xl font-bold">{count}</p>
                                                            <p className="text-xs text-slate-400 capitalize">{cls}s</p>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

export default DetectionResults

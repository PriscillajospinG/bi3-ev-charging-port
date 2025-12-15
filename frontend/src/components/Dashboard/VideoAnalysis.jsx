import React, { useState } from 'react';
import { Upload, Video, CheckCircle, AlertCircle, Loader } from 'lucide-react';

const VideoAnalysis = () => {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [processing, setProcessing] = useState(false);
    const [resultUrl, setResultUrl] = useState(null);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
            setError(null);
            setResultUrl(null);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            // Use config or relative path if proxy is working
            // Ideally use the api service, but direct fetch for multipart is often easier
            // Assuming Vite proxy forwards /api to backend
            const response = await fetch('/api/video/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Upload failed');
            }

            const data = await response.json();
            console.log('Upload success:', data);

            // Backend returns output_video_url immediately, but processing is async background
            // For UX, we show "Processing" for a few seconds then show the video
            // In a real app we'd poll status. Here we set URL but maybe wait to load it.
            setProcessing(true);
            setResultUrl(data.output_video_url);

            // Simulate waiting for processing (since we don't have real polling yet)
            // The video won't support range requests until it's written, so loading it immediately might 404
            setTimeout(() => {
                setProcessing(false);
                setUploading(false);
            }, 5000); // Wait 5s for short demo video

        } catch (err) {
            console.error(err);
            setError('Failed to upload video. Please try again.');
            setUploading(false);
        }
    };

    return (
        <div className="card">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold flex items-center gap-2">
                    <Video className="w-5 h-5 text-primary-500" />
                    AI Video Analysis
                </h3>
                {processing && (
                    <span className="text-sm text-yellow-500 flex items-center gap-1">
                        <Loader className="w-4 h-4 animate-spin" /> Processing...
                    </span>
                )}
            </div>

            <div className="space-y-4">
                {/* Upload Area */}
                <div className="border-2 border-dashed border-slate-700 rounded-lg p-6 text-center hover:border-primary-500 transition-colors">
                    <input
                        type="file"
                        id="video-upload"
                        className="hidden"
                        accept="video/*"
                        onChange={handleFileChange}
                    />
                    <label htmlFor="video-upload" className="cursor-pointer block">
                        {file ? (
                            <div className="flex items-center justify-center gap-2 text-green-400">
                                <CheckCircle className="w-5 h-5" />
                                <span>{file.name}</span>
                            </div>
                        ) : (
                            <div className="flex flex-col items-center gap-2 text-slate-400">
                                <Upload className="w-8 h-8 mb-2" />
                                <span className="text-sm">Click to upload traffic footage</span>
                                <span className="text-xs text-slate-500">MP4, AVI (Max 50MB)</span>
                            </div>
                        )}
                    </label>
                </div>

                {/* Action Button */}
                {file && !uploading && !resultUrl && (
                    <button
                        onClick={handleUpload}
                        disabled={uploading}
                        className="w-full btn-primary flex items-center justify-center gap-2"
                    >
                        Start Analysis
                    </button>
                )}

                {/* Error */}
                {error && (
                    <div className="p-3 bg-red-500/10 border border-red-500/20 rounded text-red-400 text-sm flex items-center gap-2">
                        <AlertCircle className="w-4 h-4" />
                        {error}
                    </div>
                )}

                {/* Result Video */}
                {resultUrl && !processing && (
                    <div className="mt-4 animate-fadeIn">
                        <h4 className="text-sm font-semibold mb-2 text-slate-300">Processed Output:</h4>
                        <div className="relative rounded-lg overflow-hidden bg-black aspect-video">
                            <video
                                src={resultUrl}
                                controls
                                className="w-full h-full"
                                onError={(e) => console.error("Video load error", e)}
                            />
                        </div>
                        <p className="text-xs text-slate-500 mt-2 text-center">
                            Vehicle detections highlighted in green. Check Database for events.
                        </p>
                    </div>
                )}

                {/* Processing State Placeholder */}
                {resultUrl && processing && (
                    <div className="mt-4 animate-pulse">
                        <div className="bg-slate-800 aspect-video rounded-lg flex items-center justify-center">
                            <p className="text-slate-500">Analyzing Frames...</p>
                        </div>
                    </div>
                )}

            </div>
        </div>
    );
};

export default VideoAnalysis;

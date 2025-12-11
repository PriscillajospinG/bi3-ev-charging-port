import { useState } from 'react'
import { Upload, Film } from 'lucide-react'

const VideoUpload = () => {
  const [isDragOver, setIsDragOver] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = () => {
    setIsDragOver(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragOver(false)
    
    const files = e.dataTransfer.files
    if (files.length > 0) {
      const file = files[0]
      if (isValidVideoFile(file)) {
        setSelectedFile(file)
      }
    }
  }

  const handleFileSelect = (e) => {
    const files = e.target.files
    if (files.length > 0) {
      const file = files[0]
      if (isValidVideoFile(file)) {
        setSelectedFile(file)
      }
    }
  }

  const isValidVideoFile = (file) => {
    const validTypes = ['video/mp4', 'video/quicktime', 'video/x-msvideo']
    const validExtensions = ['mp4', 'mov', 'avi']
    const fileExtension = file.name.split('.').pop().toLowerCase()
    const fileSizeMB = file.size / (1024 * 1024)

    if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
      alert('Please upload a valid video file (MP4, MOV, or AVI)')
      return false
    }

    if (fileSizeMB > 500) {
      alert('File size exceeds 500MB limit')
      return false
    }

    return true
  }

  return (
    <div className="card bg-slate-800/50 border border-slate-700">
      <div className="flex items-center gap-3 mb-4">
        <Film size={24} className="text-primary-400" />
        <h2 className="text-xl font-semibold">Upload Sample Video</h2>
      </div>

      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
          isDragOver
            ? 'border-primary-400 bg-primary-500/10'
            : 'border-slate-600 bg-slate-900/50 hover:border-slate-500'
        }`}
      >
        <Upload size={48} className="mx-auto mb-4 text-slate-400" />
        <h3 className="text-lg font-semibold mb-2">Drag and drop your video here</h3>
        <p className="text-slate-400 mb-4">or click to browse (MP4, MOV, AVI - Max 500MB)</p>
        
        <input
          type="file"
          accept="video/mp4,.mp4,video/quicktime,.mov,video/x-msvideo,.avi"
          onChange={handleFileSelect}
          className="hidden"
          id="video-input"
        />
        <label
          htmlFor="video-input"
          className="inline-block px-6 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg font-medium transition-colors cursor-pointer"
        >
          Browse Files
        </label>
      </div>

      {selectedFile && (
        <div className="mt-4 p-3 bg-success/10 border border-success/30 rounded-lg">
          <p className="text-sm text-success">
            ✓ Selected: <span className="font-semibold">{selectedFile.name}</span>
          </p>
          <p className="text-xs text-slate-400 mt-1">
            Size: {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
          </p>
        </div>
      )}
    </div>
  )
}

export default VideoUpload

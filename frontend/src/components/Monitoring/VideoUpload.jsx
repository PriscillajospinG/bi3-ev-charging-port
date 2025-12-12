import { useState } from 'react'
import { Upload, Film, FileVideo, CheckCircle, Loader } from 'lucide-react'
import { api } from '../../services/api'

const VideoUpload = () => {
  const [isDragOver, setIsDragOver] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState(null) // 'success', 'error'

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
        handleUpload(file)
      }
    }
  }

  const handleFileSelect = (e) => {
    const files = e.target.files
    if (files.length > 0) {
      const file = files[0]
      if (isValidVideoFile(file)) {
        handleUpload(file)
      }
    }
  }

  const handleUpload = async (file) => {
    setSelectedFile(file)
    setIsUploading(true)
    setUploadStatus(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await api.uploadVideo(formData)
      setUploadStatus('success')
      console.log('Upload successful:', response.data)
    } catch (e) {
      console.error("Upload failed", e)
      setUploadStatus('error')
    } finally {
      setIsUploading(false)
    }
  }

  const isValidVideoFile = (file) => {
    const validTypes = ['video/mp4', 'video/quicktime', 'video/x-msvideo']
    const validExtensions = ['mp4', 'mov', 'avi']
    const fileExtension = file.name.split('.').pop().toLowerCase()

    // Check extension and type loosely as browser mime types can vary
    if (!validExtensions.includes(fileExtension) && !validTypes.includes(file.type)) {
      alert('Please upload a valid video file (MP4, MOV, or AVI)')
      return false
    }

    if (file.size > 500 * 1024 * 1024) {
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
        className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${isDragOver
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
          disabled={isUploading}
        />
        <label
          htmlFor="video-input"
          className={`inline-block px-6 py-2 rounded-lg font-medium transition-colors cursor-pointer ${isUploading ? 'bg-slate-600 cursor-not-allowed' : 'bg-primary-600 hover:bg-primary-700'
            }`}
        >
          {isUploading ? 'Uploading...' : 'Browse Files'}
        </label>
      </div>

      {selectedFile && (
        <div className={`mt-4 p-3 border rounded-lg flex items-center gap-3 ${uploadStatus === 'error' ? 'bg-red-500/10 border-red-500/30' :
          uploadStatus === 'success' ? 'bg-success/10 border-success/30' : 'bg-slate-700/30 border-slate-600'
          }`}>
          {isUploading ? <Loader className="animate-spin text-primary-400" size={20} /> :
            uploadStatus === 'success' ? <CheckCircle className="text-success" size={20} /> :
              <FileVideo className="text-slate-400" size={20} />
          }

          <div className="flex-1">
            <p className={`text-sm ${uploadStatus === 'success' ? 'text-success' : 'text-slate-200'}`}>
              {selectedFile.name}
            </p>
            <p className="text-xs text-slate-400">
              {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
            </p>
          </div>

          {uploadStatus === 'success' && (
            <span className="text-xs font-bold text-success">
              QUEUED FOR PROCESSING ↓
            </span>
          )}
          {uploadStatus === 'error' && (
            <span className="text-xs font-bold text-red-400">
              UPLOAD FAILED
            </span>
          )}
        </div>
      )}
    </div>
  )
}

export default VideoUpload

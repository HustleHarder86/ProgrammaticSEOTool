'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, AlertCircle, CheckCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription } from '@/components/ui/alert'

interface CSVUploaderProps {
  projectId: string
  templateId?: string
  onUploadComplete: (response: UploadResponse) => void
  onError?: (error: string) => void
}

interface UploadResponse {
  dataset_id: string
  name: string
  row_count: number
  columns: string[]
  validation: {
    is_valid: boolean
    missing_columns: string[]
    warnings: string[]
  }
}

export default function CSVUploader({
  projectId,
  templateId,
  onUploadComplete,
  onError
}: CSVUploaderProps) {
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const csvFile = acceptedFiles[0]
    if (csvFile && csvFile.type === 'text/csv') {
      setFile(csvFile)
      setError(null)
    } else {
      setError('Please upload a valid CSV file')
      setFile(null)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv']
    },
    maxFiles: 1
  })

  const handleUpload = async () => {
    if (!file) return

    setIsUploading(true)
    setUploadProgress(0)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)
    if (templateId) {
      formData.append('template_id', templateId)
    }

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return prev
          }
          return prev + 10
        })
      }, 100)

      const response = await fetch(`/api/projects/${projectId}/data/upload`, {
        method: 'POST',
        body: formData
      })

      clearInterval(progressInterval)
      setUploadProgress(100)

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Upload failed')
      }

      const data: UploadResponse = await response.json()
      onUploadComplete(data)
      
      // Reset state
      setFile(null)
      setUploadProgress(0)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Upload failed'
      setError(errorMessage)
      if (onError) {
        onError(errorMessage)
      }
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="space-y-4">
      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          transition-colors duration-200
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
          ${file ? 'bg-green-50 border-green-500' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        {file ? (
          <div className="space-y-2">
            <CheckCircle className="h-12 w-12 text-green-500 mx-auto" />
            <p className="text-lg font-medium">{file.name}</p>
            <p className="text-sm text-gray-600">
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            <Upload className="h-12 w-12 text-gray-400 mx-auto" />
            <p className="text-lg font-medium">
              {isDragActive ? 'Drop your CSV file here' : 'Drag & drop your CSV file here'}
            </p>
            <p className="text-sm text-gray-600">or click to browse</p>
          </div>
        )}
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Upload Progress */}
      {isUploading && (
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>Uploading...</span>
            <span>{uploadProgress}%</span>
          </div>
          <Progress value={uploadProgress} />
        </div>
      )}

      {/* Upload Button */}
      {file && !isUploading && (
        <div className="flex justify-end gap-2">
          <Button
            variant="outline"
            onClick={() => {
              setFile(null)
              setError(null)
            }}
          >
            Cancel
          </Button>
          <Button onClick={handleUpload}>
            <Upload className="mr-2 h-4 w-4" />
            Upload CSV
          </Button>
        </div>
      )}

      {/* File Requirements */}
      <div className="bg-gray-50 rounded-lg p-4">
        <h4 className="font-medium mb-2 flex items-center">
          <FileText className="mr-2 h-4 w-4" />
          CSV File Requirements
        </h4>
        <ul className="text-sm text-gray-600 space-y-1">
          <li>• First row must contain column headers</li>
          <li>• UTF-8 encoding recommended</li>
          <li>• Maximum file size: 10MB</li>
          <li>• Supported delimiters: comma (,)</li>
        </ul>
      </div>
    </div>
  )
}
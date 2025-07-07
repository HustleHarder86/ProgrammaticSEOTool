'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import DataImportWizard from '@/components/data-import/DataImportWizard'
import DataTable from '@/components/data-import/DataTable'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Trash2, FileText, Database } from 'lucide-react'

interface DataSet {
  id: string
  name: string
  row_count: number
  columns: string[]
  created_at: string
}

interface Template {
  id: string
  name: string
  pattern: string
  variables: string[]
}

export default function DataPage() {
  const params = useParams()
  const projectId = params.id as string
  const [datasets, setDatasets] = useState<DataSet[]>([])
  const [templates, setTemplates] = useState<Template[]>([])
  const [selectedDataset, setSelectedDataset] = useState<DataSet | null>(null)
  const [isImporting, setIsImporting] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  // Load existing datasets and templates
  useEffect(() => {
    fetchDatasets()
    fetchTemplates()
  }, [projectId])

  const fetchDatasets = async () => {
    try {
      const response = await fetch(`/api/projects/${projectId}/data`)
      if (response.ok) {
        const data = await response.json()
        setDatasets(data)
      }
    } catch (error) {
      console.error('Error fetching datasets:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const fetchTemplates = async () => {
    try {
      const response = await fetch(`/api/projects/${projectId}/templates`)
      if (response.ok) {
        const data = await response.json()
        setTemplates(data)
      }
    } catch (error) {
      console.error('Error fetching templates:', error)
    }
  }

  const handleDatasetClick = async (dataset: DataSet) => {
    setSelectedDataset(dataset)
  }

  const handleDeleteDataset = async (datasetId: string) => {
    if (!confirm('Are you sure you want to delete this dataset?')) {
      return
    }

    try {
      const response = await fetch(`/api/projects/${projectId}/data/${datasetId}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        fetchDatasets()
        if (selectedDataset?.id === datasetId) {
          setSelectedDataset(null)
        }
      }
    } catch (error) {
      console.error('Error deleting dataset:', error)
    }
  }

  const handleImportComplete = () => {
    setIsImporting(false)
    fetchDatasets()
  }

  if (isLoading) {
    return (
      <div className="container mx-auto p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="h-64 bg-gray-100 rounded"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Data Management</h1>
        <p className="text-gray-600">Import and manage data for your programmatic SEO pages</p>
      </div>

      {/* Import Section */}
      {isImporting ? (
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Import Data</CardTitle>
          </CardHeader>
          <CardContent>
            <DataImportWizard
              projectId={projectId}
              templates={templates}
              onComplete={handleImportComplete}
              onCancel={() => setIsImporting(false)}
            />
          </CardContent>
        </Card>
      ) : (
        <div className="mb-8">
          <Button onClick={() => setIsImporting(true)} size="lg">
            <Database className="mr-2 h-4 w-4" />
            Import New Data
          </Button>
        </div>
      )}

      {/* Datasets Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {datasets.map((dataset) => (
          <Card
            key={dataset.id}
            className={`cursor-pointer transition-all hover:shadow-lg ${
              selectedDataset?.id === dataset.id ? 'ring-2 ring-blue-500' : ''
            }`}
            onClick={() => handleDatasetClick(dataset)}
          >
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-lg">{dataset.name}</CardTitle>
                  <p className="text-sm text-gray-500 mt-1">
                    {dataset.row_count} rows • {dataset.columns.length} columns
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation()
                    handleDeleteDataset(dataset.id)
                  }}
                >
                  <Trash2 className="h-4 w-4 text-red-500" />
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-sm">
                <p className="font-medium mb-1">Columns:</p>
                <div className="flex flex-wrap gap-1">
                  {dataset.columns.slice(0, 5).map((col) => (
                    <span
                      key={col}
                      className="px-2 py-1 bg-gray-100 rounded text-xs"
                    >
                      {col}
                    </span>
                  ))}
                  {dataset.columns.length > 5 && (
                    <span className="text-xs text-gray-500">
                      +{dataset.columns.length - 5} more
                    </span>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Data Preview */}
      {selectedDataset && (
        <Card>
          <CardHeader>
            <CardTitle>Data Preview: {selectedDataset.name}</CardTitle>
          </CardHeader>
          <CardContent>
            <DataTable
              datasetId={selectedDataset.id}
              projectId={projectId}
              limit={10}
            />
          </CardContent>
        </Card>
      )}

      {datasets.length === 0 && !isImporting && (
        <Card className="text-center py-12">
          <CardContent>
            <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium mb-2">No data imported yet</h3>
            <p className="text-gray-600 mb-4">
              Import CSV data to generate pages from your templates
            </p>
            <Button onClick={() => setIsImporting(true)}>
              Import Your First Dataset
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
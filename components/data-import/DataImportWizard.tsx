'use client'

import { useState } from 'react'
import CSVUploader from './CSVUploader'
import DataTable from './DataTable'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { 
  CheckCircle, 
  AlertCircle, 
  FileText, 
  Database,
  ArrowLeft,
  ArrowRight,
  XCircle
} from 'lucide-react'

interface DataImportWizardProps {
  projectId: string
  templates: Template[]
  onComplete: () => void
  onCancel: () => void
}

interface Template {
  id: string
  name: string
  pattern: string
  variables: string[]
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

interface ColumnMapping {
  [templateVariable: string]: string | null
}

type WizardStep = 'upload' | 'preview' | 'mapping' | 'complete'

export default function DataImportWizard({
  projectId,
  templates,
  onComplete,
  onCancel
}: DataImportWizardProps) {
  const [currentStep, setCurrentStep] = useState<WizardStep>('upload')
  const [uploadResponse, setUploadResponse] = useState<UploadResponse | null>(null)
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null)
  const [columnMappings, setColumnMappings] = useState<ColumnMapping>({})
  const [validationResult, setValidationResult] = useState<any>(null)

  const handleUploadComplete = (response: UploadResponse) => {
    setUploadResponse(response)
    setCurrentStep('preview')
  }

  const handleTemplateSelection = (template: Template) => {
    setSelectedTemplate(template)
    // Initialize column mappings
    const initialMappings: ColumnMapping = {}
    template.variables.forEach(variable => {
      // Try to auto-match columns
      const matchingColumn = uploadResponse?.columns.find(
        col => col.toLowerCase() === variable.toLowerCase()
      )
      initialMappings[variable] = matchingColumn || null
    })
    setColumnMappings(initialMappings)
  }

  const validateDataWithTemplate = async () => {
    if (!uploadResponse || !selectedTemplate) return

    try {
      const response = await fetch(
        `/api/projects/${projectId}/data/${uploadResponse.dataset_id}/validate`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ template_id: selectedTemplate.id })
        }
      )

      if (response.ok) {
        const validation = await response.json()
        setValidationResult(validation)
        setCurrentStep('mapping')
      }
    } catch (error) {
      console.error('Validation error:', error)
    }
  }

  const steps = [
    { id: 'upload', label: 'Upload CSV', icon: FileText },
    { id: 'preview', label: 'Preview Data', icon: Database },
    { id: 'mapping', label: 'Map Columns', icon: ArrowRight },
    { id: 'complete', label: 'Complete', icon: CheckCircle }
  ]

  const currentStepIndex = steps.findIndex(s => s.id === currentStep)

  return (
    <div className="space-y-6">
      {/* Progress Steps */}
      <div className="flex items-center justify-between mb-8">
        {steps.map((step, index) => {
          const Icon = step.icon
          const isActive = step.id === currentStep
          const isCompleted = index < currentStepIndex
          
          return (
            <div key={step.id} className="flex items-center flex-1">
              <div className="flex items-center">
                <div
                  className={`
                    w-10 h-10 rounded-full flex items-center justify-center
                    ${isActive ? 'bg-blue-500 text-white' : ''}
                    ${isCompleted ? 'bg-green-500 text-white' : ''}
                    ${!isActive && !isCompleted ? 'bg-gray-200 text-gray-500' : ''}
                  `}
                >
                  <Icon className="h-5 w-5" />
                </div>
                <span className={`ml-2 text-sm font-medium ${isActive ? 'text-blue-600' : 'text-gray-600'}`}>
                  {step.label}
                </span>
              </div>
              {index < steps.length - 1 && (
                <div className={`flex-1 h-0.5 mx-4 ${isCompleted ? 'bg-green-500' : 'bg-gray-200'}`} />
              )}
            </div>
          )
        })}
      </div>

      {/* Step Content */}
      {currentStep === 'upload' && (
        <div>
          <h3 className="text-lg font-semibold mb-4">Upload Your CSV Data</h3>
          <CSVUploader
            projectId={projectId}
            onUploadComplete={handleUploadComplete}
          />
        </div>
      )}

      {currentStep === 'preview' && uploadResponse && (
        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-4">Data Preview</h3>
            <Card>
              <CardContent className="pt-6">
                <div className="grid grid-cols-3 gap-4 mb-6">
                  <div>
                    <p className="text-sm text-gray-600">Dataset Name</p>
                    <p className="font-medium">{uploadResponse.name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Total Rows</p>
                    <p className="font-medium">{uploadResponse.row_count}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Columns</p>
                    <p className="font-medium">{uploadResponse.columns.length}</p>
                  </div>
                </div>
                
                <DataTable
                  datasetId={uploadResponse.dataset_id}
                  projectId={projectId}
                  limit={5}
                  showPagination={false}
                />
              </CardContent>
            </Card>
          </div>

          {templates.length > 0 && (
            <div>
              <h4 className="font-medium mb-3">Select a template to validate against (optional)</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {templates.map((template) => (
                  <Card
                    key={template.id}
                    className={`cursor-pointer transition-all ${
                      selectedTemplate?.id === template.id
                        ? 'ring-2 ring-blue-500'
                        : 'hover:shadow-md'
                    }`}
                    onClick={() => handleTemplateSelection(template)}
                  >
                    <CardContent className="p-4">
                      <h5 className="font-medium">{template.name}</h5>
                      <p className="text-sm text-gray-600 mt-1">{template.pattern}</p>
                      <div className="mt-2">
                        <p className="text-xs text-gray-500">Required variables:</p>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {template.variables.map((variable) => (
                            <span
                              key={variable}
                              className="px-2 py-0.5 bg-gray-100 rounded text-xs"
                            >
                              {variable}
                            </span>
                          ))}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {currentStep === 'mapping' && selectedTemplate && validationResult && (
        <div className="space-y-6">
          <h3 className="text-lg font-semibold">Column Mapping</h3>
          
          {/* Validation Status */}
          {validationResult.is_valid ? (
            <Alert>
              <CheckCircle className="h-4 w-4 text-green-500" />
              <AlertDescription>
                All required variables have matching columns in your data!
              </AlertDescription>
            </Alert>
          ) : (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                Missing columns: {validationResult.missing_columns.join(', ')}
              </AlertDescription>
            </Alert>
          )}

          {/* Mapping Suggestions */}
          <Card>
            <CardContent className="pt-6">
              <h4 className="font-medium mb-4">Column Mappings</h4>
              <div className="space-y-3">
                {selectedTemplate.variables.map((variable) => {
                  const suggestion = validationResult.column_mapping_suggestions[variable]
                  return (
                    <div key={variable} className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{variable}</span>
                        <ArrowRight className="h-4 w-4 text-gray-400" />
                      </div>
                      <div className="flex items-center gap-2">
                        {suggestion ? (
                          <>
                            <span className="text-green-600">{suggestion}</span>
                            <CheckCircle className="h-4 w-4 text-green-500" />
                          </>
                        ) : (
                          <>
                            <span className="text-red-600">No match found</span>
                            <XCircle className="h-4 w-4 text-red-500" />
                          </>
                        )}
                      </div>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>

          {validationResult.warnings.length > 0 && (
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                <p className="font-medium mb-1">Warnings:</p>
                <ul className="list-disc list-inside">
                  {validationResult.warnings.map((warning: string, index: number) => (
                    <li key={index} className="text-sm">{warning}</li>
                  ))}
                </ul>
              </AlertDescription>
            </Alert>
          )}
        </div>
      )}

      {currentStep === 'complete' && (
        <div className="text-center py-8">
          <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">Data Import Complete!</h3>
          <p className="text-gray-600 mb-6">
            Your data has been successfully imported and is ready to use.
          </p>
          <Button onClick={onComplete}>
            View All Datasets
          </Button>
        </div>
      )}

      {/* Navigation Buttons */}
      <div className="flex justify-between pt-6 border-t">
        <Button
          variant="outline"
          onClick={() => {
            if (currentStep === 'upload') {
              onCancel()
            } else if (currentStep === 'preview') {
              setCurrentStep('upload')
            } else if (currentStep === 'mapping') {
              setCurrentStep('preview')
            }
          }}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          {currentStep === 'upload' ? 'Cancel' : 'Back'}
        </Button>

        <Button
          onClick={() => {
            if (currentStep === 'preview') {
              if (selectedTemplate) {
                validateDataWithTemplate()
              } else {
                setCurrentStep('complete')
              }
            } else if (currentStep === 'mapping') {
              setCurrentStep('complete')
            }
          }}
          disabled={
            (currentStep === 'preview' && !uploadResponse) ||
            (currentStep === 'mapping' && !validationResult?.is_valid && selectedTemplate)
          }
        >
          {currentStep === 'mapping' && !validationResult?.is_valid
            ? 'Fix Mapping Issues'
            : currentStep === 'complete'
            ? 'Done'
            : 'Continue'}
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}
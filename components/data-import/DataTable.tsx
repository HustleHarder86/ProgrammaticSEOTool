'use client'

import { useState, useEffect, useCallback } from 'react'
import { ChevronLeft, ChevronRight, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

interface DataTableProps {
  datasetId: string
  projectId: string
  limit?: number
  showPagination?: boolean
}

interface DatasetDetail {
  id: string
  name: string
  data: Record<string, unknown>[]
  row_count: number
  columns: string[]
}

export default function DataTable({
  datasetId,
  projectId,
  limit = 10,
  showPagination = true
}: DataTableProps) {
  const [dataset, setDataset] = useState<DatasetDetail | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [currentPage, setCurrentPage] = useState(1)
  const [error, setError] = useState<string | null>(null)

  const fetchDataset = useCallback(async () => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch(`/api/projects/${projectId}/data/${datasetId}`)
      if (!response.ok) {
        throw new Error('Failed to fetch dataset')
      }
      const data = await response.json()
      setDataset(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data')
    } finally {
      setIsLoading(false)
    }
  }, [datasetId, projectId])

  useEffect(() => {
    fetchDataset()
  }, [fetchDataset])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-500">Error: {error}</p>
      </div>
    )
  }

  if (!dataset || dataset.data.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No data available</p>
      </div>
    )
  }

  const totalPages = Math.ceil(dataset.row_count / limit)
  const startIdx = (currentPage - 1) * limit
  const endIdx = startIdx + limit
  const displayData = showPagination 
    ? dataset.data.slice(startIdx, endIdx)
    : dataset.data.slice(0, limit)

  return (
    <div className="space-y-4">
      {/* Table Info */}
      <div className="flex justify-between items-center text-sm text-gray-600">
        <span>
          Showing {startIdx + 1}-{Math.min(endIdx, dataset.row_count)} of {dataset.row_count} rows
        </span>
        <span>{dataset.columns.length} columns</span>
      </div>

      {/* Data Table */}
      <div className="border rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                {dataset.columns.map((column) => (
                  <TableHead key={column} className="font-medium">
                    {column}
                  </TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {displayData.map((row, rowIndex) => (
                <TableRow key={rowIndex}>
                  {dataset.columns.map((column) => (
                    <TableCell key={column} className="max-w-xs truncate">
                      {row[column] !== null && row[column] !== undefined
                        ? String(row[column])
                        : <span className="text-gray-400">-</span>}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>

      {/* Pagination */}
      {showPagination && totalPages > 1 && (
        <div className="flex items-center justify-between">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setCurrentPage(currentPage - 1)}
            disabled={currentPage === 1}
          >
            <ChevronLeft className="h-4 w-4 mr-1" />
            Previous
          </Button>
          
          <div className="text-sm text-gray-600">
            Page {currentPage} of {totalPages}
          </div>
          
          <Button
            variant="outline"
            size="sm"
            onClick={() => setCurrentPage(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            Next
            <ChevronRight className="h-4 w-4 ml-1" />
          </Button>
        </div>
      )}

      {/* Preview Note */}
      {!showPagination && dataset.row_count > limit && (
        <p className="text-sm text-gray-500 text-center">
          Showing first {limit} rows of {dataset.row_count} total
        </p>
      )}
    </div>
  )
}
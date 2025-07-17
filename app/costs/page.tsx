'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ArrowLeft, DollarSign, TrendingUp, BarChart3, Info } from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'
// Select component will be replaced with native HTML select

interface CostSummary {
  project_id: string
  project_name: string
  total_cost: number
  total_tokens: number
  total_calls: number
}

interface ProjectCostDetails {
  project_id: string
  total_cost: number
  total_tokens: number
  total_calls: number
  by_operation: Record<string, {
    count: number
    cost: number
    tokens: number
  }>
  by_provider: Record<string, {
    count: number
    cost: number
    tokens: number
  }>
  period: {
    start: string | null
    end: string | null
  }
}

export default function CostsPage() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [projectSummaries, setProjectSummaries] = useState<CostSummary[]>([])
  const [selectedProject, setSelectedProject] = useState<string | null>(null)
  const [projectDetails, setProjectDetails] = useState<ProjectCostDetails | null>(null)
  const [days, setDays] = useState<number>(30)
  const [pricing, setPricing] = useState<any>(null)

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  useEffect(() => {
    fetchCostSummaries()
    fetchPricing()
  }, [days])

  useEffect(() => {
    if (selectedProject) {
      fetchProjectDetails(selectedProject)
    }
  }, [selectedProject, days])

  const fetchCostSummaries = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/costs/projects?days=${days}`)
      if (!response.ok) throw new Error('Failed to fetch cost summaries')
      const data = await response.json()
      setProjectSummaries(data)
      setLoading(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load cost data')
      setLoading(false)
    }
  }

  const fetchProjectDetails = async (projectId: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/costs/projects/${projectId}?days=${days}`)
      if (!response.ok) throw new Error('Failed to fetch project details')
      const data = await response.json()
      setProjectDetails(data)
    } catch (err) {
      console.error('Failed to fetch project details:', err)
    }
  }

  const fetchPricing = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/costs/pricing`)
      if (!response.ok) throw new Error('Failed to fetch pricing')
      const data = await response.json()
      setPricing(data)
    } catch (err) {
      console.error('Failed to fetch pricing:', err)
    }
  }

  const formatCost = (cost: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 4
    }).format(cost)
  }

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US').format(num)
  }

  const totalCosts = projectSummaries.reduce((sum, project) => sum + project.total_cost, 0)
  const totalTokens = projectSummaries.reduce((sum, project) => sum + project.total_tokens, 0)
  const totalCalls = projectSummaries.reduce((sum, project) => sum + project.total_calls, 0)

  if (loading) {
    return (
      <div className="container mx-auto p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-32 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container mx-auto p-6">
        <Alert>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6 max-w-7xl">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <Link href="/">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="h-4 w-4" />
            </Button>
          </Link>
          <h1 className="text-3xl font-bold">API Cost Tracking</h1>
        </div>
        <select 
          value={days.toString()} 
          onChange={(e) => setDays(parseInt(e.target.value))}
          className="w-[180px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="7">Last 7 days</option>
          <option value="30">Last 30 days</option>
          <option value="90">Last 90 days</option>
          <option value="365">Last year</option>
        </select>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Cost</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCost(totalCosts)}</div>
            <p className="text-xs text-muted-foreground">
              Across {projectSummaries.length} projects
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Tokens</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatNumber(totalTokens)}</div>
            <p className="text-xs text-muted-foreground">
              {formatNumber(totalCalls)} API calls
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Cost</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatCost(totalCalls > 0 ? totalCosts / totalCalls : 0)}
            </div>
            <p className="text-xs text-muted-foreground">Per API call</p>
          </CardContent>
        </Card>
      </div>

      {/* Project List */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Projects</CardTitle>
          <CardDescription>Click on a project to see detailed cost breakdown</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {projectSummaries.length === 0 ? (
              <p className="text-muted-foreground">No API usage recorded yet</p>
            ) : (
              projectSummaries.map((project) => (
                <div
                  key={project.project_id}
                  className={`p-4 rounded-lg border cursor-pointer transition-colors ${
                    selectedProject === project.project_id
                      ? 'border-primary bg-primary/5'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => setSelectedProject(project.project_id)}
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <h3 className="font-semibold">{project.project_name}</h3>
                      <p className="text-sm text-muted-foreground">
                        {formatNumber(project.total_calls)} calls • {formatNumber(project.total_tokens)} tokens
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold">{formatCost(project.total_cost)}</p>
                      <p className="text-xs text-muted-foreground">
                        {formatCost(project.total_calls > 0 ? project.total_cost / project.total_calls : 0)}/call
                      </p>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      {/* Project Details */}
      {selectedProject && projectDetails && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card>
            <CardHeader>
              <CardTitle>Cost by Operation</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {Object.entries(projectDetails.by_operation).map(([operation, data]) => (
                  <div key={operation} className="flex justify-between items-center">
                    <div>
                      <p className="font-medium capitalize">
                        {operation.replace(/_/g, ' ')}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {data.count} calls • {formatNumber(data.tokens)} tokens
                      </p>
                    </div>
                    <p className="font-semibold">{formatCost(data.cost)}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Cost by Provider</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {Object.entries(projectDetails.by_provider).map(([provider, data]) => (
                  <div key={provider} className="flex justify-between items-center">
                    <div>
                      <p className="font-medium capitalize">{provider}</p>
                      <p className="text-sm text-muted-foreground">
                        {data.count} calls • {formatNumber(data.tokens)} tokens
                      </p>
                    </div>
                    <p className="font-semibold">{formatCost(data.cost)}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Pricing Info */}
      {pricing && (
        <Card className="mt-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Info className="h-4 w-4" />
              Current Pricing
            </CardTitle>
            <CardDescription>Cost per 1,000 tokens in USD</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {Object.entries(pricing.pricing).map(([provider, models]: [string, any]) => (
                <div key={provider}>
                  <h4 className="font-semibold capitalize mb-2">{provider}</h4>
                  <div className="space-y-1">
                    {Object.entries(models).map(([model, prices]: [string, any]) => (
                      <div key={model} className="text-sm">
                        <span className="text-muted-foreground">{model}:</span>
                        <span className="ml-2">
                          ${prices.input}/in • ${prices.output}/out
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
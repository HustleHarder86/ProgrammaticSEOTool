"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Search, CheckSquare, Square, Info } from 'lucide-react';

interface TitlePreviewProps {
  titles: string[];
  onSelectionChange: (selectedTitles: string[]) => void;
  onGeneratePages: (selectedTitles: string[]) => void;
}

export default function TitlePreview({
  titles,
  onSelectionChange,
  onGeneratePages
}: TitlePreviewProps) {
  const [selectedTitles, setSelectedTitles] = useState<Set<string>>(new Set(titles));
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const titlesPerPage = 50;

  // Filter titles based on search
  const filteredTitles = titles.filter(title =>
    title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Pagination
  const totalPages = Math.ceil(filteredTitles.length / titlesPerPage);
  const startIndex = (currentPage - 1) * titlesPerPage;
  const displayedTitles = filteredTitles.slice(startIndex, startIndex + titlesPerPage);

  useEffect(() => {
    onSelectionChange(Array.from(selectedTitles));
  }, [selectedTitles, onSelectionChange]);

  const handleSelectAll = () => {
    setSelectedTitles(new Set(titles));
  };

  const handleDeselectAll = () => {
    setSelectedTitles(new Set());
  };

  const handleSelectFiltered = () => {
    const newSelection = new Set(selectedTitles);
    filteredTitles.forEach(title => newSelection.add(title));
    setSelectedTitles(newSelection);
  };

  const handleDeselectFiltered = () => {
    const newSelection = new Set(selectedTitles);
    filteredTitles.forEach(title => newSelection.delete(title));
    setSelectedTitles(newSelection);
  };

  const toggleTitle = (title: string) => {
    const newSelection = new Set(selectedTitles);
    if (newSelection.has(title)) {
      newSelection.delete(title);
    } else {
      newSelection.add(title);
    }
    setSelectedTitles(newSelection);
  };

  const handleGenerateClick = () => {
    onGeneratePages(Array.from(selectedTitles));
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Review and Select Pages to Generate</CardTitle>
          <CardDescription>
            {titles.length} potential pages • {selectedTitles.size} selected
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Search and Bulk Actions */}
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <input
                type="text"
                placeholder="Search titles..."
                value={searchTerm}
                onChange={(e) => {
                  setSearchTerm(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full pl-10 pr-4 py-2 border rounded-md"
              />
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleSelectAll}
              >
                <CheckSquare className="mr-1 h-4 w-4" />
                Select All
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleDeselectAll}
              >
                <Square className="mr-1 h-4 w-4" />
                Deselect All
              </Button>
              {searchTerm && (
                <>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleSelectFiltered}
                  >
                    Select Filtered
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleDeselectFiltered}
                  >
                    Deselect Filtered
                  </Button>
                </>
              )}
            </div>
          </div>

          {/* Info Alert */}
          {selectedTitles.size === 0 && (
            <Alert>
              <Info className="h-4 w-4" />
              <AlertDescription>
                No pages selected. Select at least one page to generate.
              </AlertDescription>
            </Alert>
          )}

          {/* Title List */}
          <div className="border rounded-lg max-h-96 overflow-y-auto">
            <div className="divide-y">
              {displayedTitles.map((title, index) => (
                <div
                  key={`${title}-${index}`}
                  className="flex items-center p-3 hover:bg-gray-50 transition-colors"
                >
                  <Checkbox
                    checked={selectedTitles.has(title)}
                    onCheckedChange={() => toggleTitle(title)}
                    id={`title-${startIndex + index}`}
                  />
                  <label
                    htmlFor={`title-${startIndex + index}`}
                    className="ml-3 flex-1 cursor-pointer text-sm"
                  >
                    {title}
                  </label>
                </div>
              ))}
            </div>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-600">
                Showing {startIndex + 1}-{Math.min(startIndex + titlesPerPage, filteredTitles.length)} of {filteredTitles.length} titles
              </p>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                >
                  Previous
                </Button>
                <span className="px-3 py-2 text-sm">
                  Page {currentPage} of {totalPages}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                  disabled={currentPage === totalPages}
                >
                  Next
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Generate Button */}
      <div className="flex justify-end">
        <Button
          size="lg"
          onClick={handleGenerateClick}
          disabled={selectedTitles.size === 0}
        >
          Generate {selectedTitles.size} Selected {selectedTitles.size === 1 ? 'Page' : 'Pages'}
        </Button>
      </div>
    </div>
  );
}
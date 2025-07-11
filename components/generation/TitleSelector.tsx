"use client";

import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Filter, Hash, Zap } from 'lucide-react';

interface TitleSelectorProps {
  variableData: Record<string, string[]>;
  selectedCount: number;
  totalCount: number;
  onQuickSelect: (type: 'random' | 'first' | 'last' | 'pattern', value?: any) => void;
}

export default function TitleSelector({
  variableData,
  selectedCount,
  totalCount,
  onQuickSelect
}: TitleSelectorProps) {
  const variables = Object.keys(variableData);
  const [selectedVariable, setSelectedVariable] = React.useState(variables[0] || '');
  const [selectedValues, setSelectedValues] = React.useState<string[]>([]);

  const handleVariableSelect = (variable: string) => {
    setSelectedVariable(variable);
    setSelectedValues([]);
  };

  const handleValueToggle = (value: string) => {
    setSelectedValues(prev => {
      if (prev.includes(value)) {
        return prev.filter(v => v !== value);
      }
      return [...prev, value];
    });
  };

  const applyVariableFilter = () => {
    if (selectedValues.length > 0) {
      onQuickSelect('pattern', {
        variable: selectedVariable,
        values: selectedValues
      });
    }
  };

  return (
    <Card>
      <CardContent className="p-4 space-y-4">
        {/* Selection Stats */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Hash className="h-4 w-4 text-gray-500" />
            <span className="text-sm font-medium">
              {selectedCount} of {totalCount} pages selected
            </span>
          </div>
          <div className="text-sm text-gray-500">
            {Math.round((selectedCount / totalCount) * 100)}% selected
          </div>
        </div>

        {/* Quick Selection Buttons */}
        <div className="space-y-2">
          <p className="text-sm font-medium flex items-center gap-2">
            <Zap className="h-4 w-4 text-yellow-500" />
            Quick Selection
          </p>
          <div className="flex flex-wrap gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => onQuickSelect('first', 10)}
            >
              First 10
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => onQuickSelect('first', 25)}
            >
              First 25
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => onQuickSelect('first', 50)}
            >
              First 50
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => onQuickSelect('random', 25)}
            >
              Random 25
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => onQuickSelect('random', 50)}
            >
              Random 50
            </Button>
          </div>
        </div>

        {/* Variable-based Filtering */}
        {variables.length > 0 && (
          <div className="space-y-2">
            <p className="text-sm font-medium flex items-center gap-2">
              <Filter className="h-4 w-4 text-blue-500" />
              Filter by Variable Values
            </p>
            
            {/* Variable Tabs */}
            <div className="flex gap-2 flex-wrap">
              {variables.map(variable => (
                <Button
                  key={variable}
                  variant={selectedVariable === variable ? "default" : "outline"}
                  size="sm"
                  onClick={() => handleVariableSelect(variable)}
                >
                  {variable}
                </Button>
              ))}
            </div>

            {/* Values for Selected Variable */}
            {selectedVariable && variableData[selectedVariable] && (
              <div className="border rounded-lg p-3 max-h-40 overflow-y-auto">
                <div className="flex flex-wrap gap-2">
                  {variableData[selectedVariable].slice(0, 20).map(value => (
                    <Badge
                      key={value}
                      variant={selectedValues.includes(value) ? "default" : "outline"}
                      className="cursor-pointer"
                      onClick={() => handleValueToggle(value)}
                    >
                      {value}
                    </Badge>
                  ))}
                  {variableData[selectedVariable].length > 20 && (
                    <Badge variant="secondary">
                      +{variableData[selectedVariable].length - 20} more
                    </Badge>
                  )}
                </div>
              </div>
            )}

            {/* Apply Filter Button */}
            {selectedValues.length > 0 && (
              <Button
                size="sm"
                onClick={applyVariableFilter}
                className="w-full"
              >
                Select pages with {selectedVariable}: {selectedValues.join(', ')}
              </Button>
            )}
          </div>
        )}

        {/* Selection Tips */}
        <div className="text-xs text-gray-500 space-y-1">
          <p>💡 Tips:</p>
          <ul className="list-disc list-inside space-y-0.5 ml-2">
            <li>Start with a smaller selection to test your template</li>
            <li>Use filters to select specific variable combinations</li>
            <li>You can always generate more pages later</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  );
}
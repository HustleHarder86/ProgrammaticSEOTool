"""Data processing functionality for handling CSV uploads and data management."""
import pandas as pd
import io
import json
from typing import List, Dict, Any, Optional, Tuple
from fastapi import UploadFile, HTTPException
import chardet

class DataProcessor:
    """Handles CSV parsing, validation, and data processing."""
    
    def __init__(self):
        self.max_file_size = 10 * 1024 * 1024  # 10MB max file size
        self.supported_encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
    
    async def process_csv_upload(self, file: UploadFile) -> Tuple[List[Dict[str, Any]], List[str], int]:
        """
        Process an uploaded CSV file.
        
        Returns:
            - data: List of dictionaries (each row as a dict)
            - columns: List of column names
            - row_count: Number of data rows (excluding header)
        """
        # Validate file extension
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > self.max_file_size:
            raise HTTPException(status_code=400, detail=f"File too large. Maximum size is {self.max_file_size // 1024 // 1024}MB")
        
        # Detect encoding
        encoding = self._detect_encoding(content)
        
        try:
            # Try to parse CSV with detected encoding
            df = pd.read_csv(io.BytesIO(content), encoding=encoding)
        except Exception as e:
            # Try alternative encodings
            for alt_encoding in self.supported_encodings:
                if alt_encoding != encoding:
                    try:
                        df = pd.read_csv(io.BytesIO(content), encoding=alt_encoding)
                        encoding = alt_encoding
                        break
                    except:
                        continue
            else:
                raise HTTPException(status_code=400, detail=f"Failed to parse CSV file. Error: {str(e)}")
        
        # Validate data
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
        if len(df.columns) == 0:
            raise HTTPException(status_code=400, detail="No columns found in CSV")
        
        # Clean column names
        df.columns = [self._clean_column_name(col) for col in df.columns]
        
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Convert NaN to None for JSON serialization
        df = df.where(pd.notna(df), None)
        
        # Convert to list of dictionaries
        data = df.to_dict('records')
        columns = df.columns.tolist()
        row_count = len(data)
        
        return data, columns, row_count
    
    def _detect_encoding(self, content: bytes) -> str:
        """Detect the encoding of the file content."""
        # Try chardet detection
        detection = chardet.detect(content)
        if detection['confidence'] > 0.7:
            return detection['encoding'].lower()
        
        # Default to utf-8
        return 'utf-8'
    
    def _clean_column_name(self, col_name: str) -> str:
        """Clean and standardize column names."""
        # Convert to string if not already
        col_name = str(col_name)
        
        # Remove leading/trailing whitespace
        col_name = col_name.strip()
        
        # Replace spaces with underscores
        col_name = col_name.replace(' ', '_')
        
        # Remove special characters except underscores
        col_name = ''.join(c for c in col_name if c.isalnum() or c == '_')
        
        # Ensure it doesn't start with a number
        if col_name and col_name[0].isdigit():
            col_name = f"col_{col_name}"
        
        # If empty, generate a name
        if not col_name:
            col_name = "unnamed_column"
        
        return col_name.lower()
    
    def validate_data_for_template(self, data: List[Dict[str, Any]], required_variables: List[str]) -> Dict[str, Any]:
        """
        Validate that the data contains all required variables for a template.
        
        Returns:
            - is_valid: Boolean indicating if data is valid
            - missing_columns: List of missing required columns
            - warnings: List of warning messages
        """
        if not data:
            return {
                "is_valid": False,
                "missing_columns": required_variables,
                "warnings": ["No data provided"]
            }
        
        # Get columns from first row
        columns = list(data[0].keys())
        
        # Check for missing required variables
        missing_columns = [var for var in required_variables if var not in columns]
        
        # Generate warnings
        warnings = []
        
        # Check for empty values in required columns
        for var in required_variables:
            if var in columns:
                empty_count = sum(1 for row in data if not row.get(var))
                if empty_count > 0:
                    warnings.append(f"Column '{var}' has {empty_count} empty values")
        
        # Check for duplicate values (which might limit unique pages)
        for var in required_variables:
            if var in columns:
                values = [row.get(var) for row in data if row.get(var)]
                unique_values = set(values)
                if len(unique_values) < len(values):
                    warnings.append(f"Column '{var}' has duplicate values ({len(unique_values)} unique out of {len(values)})")
        
        return {
            "is_valid": len(missing_columns) == 0,
            "missing_columns": missing_columns,
            "warnings": warnings
        }
    
    def get_column_mapping_suggestions(self, data_columns: List[str], template_variables: List[str]) -> Dict[str, Optional[str]]:
        """
        Suggest column mappings from data columns to template variables.
        Uses fuzzy matching to find best matches.
        """
        suggestions = {}
        
        for var in template_variables:
            var_lower = var.lower()
            best_match = None
            best_score = 0
            
            for col in data_columns:
                col_lower = col.lower()
                
                # Exact match
                if var_lower == col_lower:
                    best_match = col
                    break
                
                # Partial match
                if var_lower in col_lower or col_lower in var_lower:
                    score = len(var_lower) / max(len(var_lower), len(col_lower))
                    if score > best_score:
                        best_score = score
                        best_match = col
            
            suggestions[var] = best_match
        
        return suggestions
    
    def prepare_data_for_storage(self, data: List[Dict[str, Any]], name: str) -> Dict[str, Any]:
        """
        Prepare data for storage in the database.
        
        Returns formatted data structure for DataSet model.
        """
        # Ensure all rows have the same keys
        all_keys = set()
        for row in data:
            all_keys.update(row.keys())
        
        # Normalize data - ensure all rows have all keys
        normalized_data = []
        for row in data:
            normalized_row = {key: row.get(key, None) for key in all_keys}
            normalized_data.append(normalized_row)
        
        return {
            "name": name,
            "data": normalized_data,
            "row_count": len(normalized_data),
            "columns": sorted(list(all_keys))
        }
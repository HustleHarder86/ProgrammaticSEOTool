"""Data Manager Agent - Handles all data import, validation, and management for programmatic SEO"""
import csv
import json
import pandas as pd
import re
from typing import List, Dict, Any, Optional, Tuple, Set
from pathlib import Path
import chardet
from datetime import datetime
import itertools
from collections import Counter
import unicodedata
import logging

logger = logging.getLogger(__name__)

class DataManagerAgent:
    """
    Agent responsible for handling all data operations including:
    - CSV and JSON import with intelligent detection
    - Data validation and cleaning
    - Data type detection and template suggestions
    - Data transformations and enrichment
    - Multiple data source merging
    - Quality checks and statistics
    """
    
    def __init__(self):
        """Initialize the Data Manager Agent"""
        self.data_sets = {}
        self.data_statistics = {}
        self.validation_rules = self._initialize_validation_rules()
        
    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialize validation rules for different data types"""
        return {
            "location": {
                "max_length": 100,
                "allowed_chars": r'^[a-zA-Z0-9\s\-,\.\'&]+$',
                "min_length": 2,
                "check_duplicates": True,
                "normalize": True
            },
            "service": {
                "max_length": 80,
                "allowed_chars": r'^[a-zA-Z0-9\s\-&\'\./]+$',
                "min_length": 2,
                "check_duplicates": True,
                "normalize": True
            },
            "product": {
                "max_length": 100,
                "allowed_chars": r'^[a-zA-Z0-9\s\-&\'\./\+]+$',
                "min_length": 2,
                "check_duplicates": True,
                "normalize": True
            },
            "generic": {
                "max_length": 200,
                "allowed_chars": r'^[a-zA-Z0-9\s\-,\.\'&\(\)/]+$',
                "min_length": 1,
                "check_duplicates": True,
                "normalize": True
            }
        }
    
    def import_csv(
        self,
        file_path: str,
        data_type: Optional[str] = None,
        encoding: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Import data from CSV file with intelligent column detection
        
        Args:
            file_path: Path to CSV file
            data_type: Optional data type hint
            encoding: Optional encoding (auto-detected if not provided)
            
        Returns:
            Import results with data and statistics
        """
        try:
            # Auto-detect encoding if not provided
            if not encoding:
                encoding = self._detect_encoding(file_path)
            
            # Read CSV file
            df = pd.read_csv(file_path, encoding=encoding)
            
            # Detect column types and data structure
            column_analysis = self._analyze_columns(df)
            
            # Process each column
            imported_data = {}
            validation_results = {}
            
            for column_name, column_info in column_analysis.items():
                # Clean column name
                clean_name = self._clean_column_name(column_name)
                
                # Extract and clean values
                values = df[column_name].dropna().astype(str).tolist()
                
                # Validate and clean data
                cleaned_values, validation = self.validate_data(
                    values,
                    data_type=column_info['suggested_type']
                )
                
                imported_data[clean_name] = cleaned_values
                validation_results[clean_name] = validation
            
            # Store data
            self._store_data(imported_data)
            
            # Generate statistics
            statistics = self._generate_import_statistics(imported_data, validation_results)
            
            return {
                "success": True,
                "data": imported_data,
                "column_analysis": column_analysis,
                "validation_results": validation_results,
                "statistics": statistics,
                "encoding_used": encoding
            }
            
        except Exception as e:
            logger.error(f"CSV import failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "suggestions": self._get_import_error_suggestions(str(e))
            }
    
    def import_json(self, file_path: str) -> Dict[str, Any]:
        """
        Import data from JSON file
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Import results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            imported_data = {}
            
            if isinstance(data, dict):
                # Process dictionary structure
                for key, values in data.items():
                    if isinstance(values, list):
                        # Clean and validate list data
                        cleaned_values, validation = self.validate_data(
                            [str(v) for v in values],
                            data_type=self._detect_data_type(key, values)
                        )
                        imported_data[key] = cleaned_values
                    elif isinstance(values, dict):
                        # Flatten nested structures
                        flattened = self._flatten_dict(values, key)
                        imported_data.update(flattened)
            elif isinstance(data, list):
                # Handle array of objects
                imported_data = self._process_json_array(data)
            
            # Store data
            self._store_data(imported_data)
            
            # Generate statistics
            statistics = self._generate_import_statistics(imported_data, {})
            
            return {
                "success": True,
                "data": imported_data,
                "statistics": statistics
            }
            
        except Exception as e:
            logger.error(f"JSON import failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def add_data_manually(
        self,
        data_type: str,
        values: List[str],
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add data entries manually
        
        Args:
            data_type: Type of data (location, service, product, etc.)
            values: List of values to add
            name: Optional name for the data set
            
        Returns:
            Results of manual data addition
        """
        # Use provided name or generate from data_type
        dataset_name = name or data_type
        
        # Validate and clean data
        cleaned_values, validation = self.validate_data(values, data_type)
        
        # Store data
        self.data_sets[dataset_name] = cleaned_values
        
        # Update statistics
        self.data_statistics[dataset_name] = {
            "count": len(cleaned_values),
            "unique_count": len(set(cleaned_values)),
            "type": data_type,
            "added_at": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "dataset_name": dataset_name,
            "cleaned_values": cleaned_values,
            "validation": validation,
            "statistics": self.data_statistics[dataset_name]
        }
    
    def validate_data(
        self,
        data: List[str],
        data_type: Optional[str] = None
    ) -> Tuple[List[str], Dict[str, Any]]:
        """
        Validate and clean data according to SEO best practices
        
        Args:
            data: List of values to validate
            data_type: Type of data for specific validation rules
            
        Returns:
            Tuple of (cleaned_data, validation_results)
        """
        # Get validation rules
        rules = self.validation_rules.get(data_type, self.validation_rules["generic"])
        
        cleaned_data = []
        issues = {
            "duplicates": [],
            "invalid_chars": [],
            "too_long": [],
            "too_short": [],
            "empty": 0,
            "special_chars_removed": []
        }
        
        seen = set()
        seen_normalized = set()
        
        for value in data:
            # Skip empty values
            if not value or not str(value).strip():
                issues["empty"] += 1
                continue
            
            value_str = str(value).strip()
            
            # Check length
            if len(value_str) > rules["max_length"]:
                issues["too_long"].append(value_str)
                value_str = value_str[:rules["max_length"]]
            elif len(value_str) < rules["min_length"]:
                issues["too_short"].append(value_str)
                continue
            
            # Normalize if required
            if rules.get("normalize", True):
                normalized = self._normalize_value(value_str)
            else:
                normalized = value_str
            
            # Check for duplicates
            normalized_lower = normalized.lower()
            if rules["check_duplicates"] and normalized_lower in seen_normalized:
                issues["duplicates"].append(value_str)
                continue
            
            # Validate characters
            if not re.match(rules["allowed_chars"], normalized):
                # Try to clean special characters
                cleaned = self._clean_special_chars(normalized)
                if re.match(rules["allowed_chars"], cleaned):
                    issues["special_chars_removed"].append({
                        "original": value_str,
                        "cleaned": cleaned
                    })
                    normalized = cleaned
                else:
                    issues["invalid_chars"].append(value_str)
                    continue
            
            cleaned_data.append(normalized)
            seen.add(value_str)
            seen_normalized.add(normalized_lower)
        
        validation_results = {
            "original_count": len(data),
            "cleaned_count": len(cleaned_data),
            "issues": issues,
            "is_valid": len(issues["invalid_chars"]) == 0,
            "warnings": self._generate_warnings(issues),
            "data_quality_score": self._calculate_quality_score(len(data), len(cleaned_data), issues)
        }
        
        return cleaned_data, validation_results
    
    def detect_data_types(self, data_sets: Dict[str, List[str]]) -> Dict[str, str]:
        """
        Intelligently detect data types and suggest appropriate templates
        
        Args:
            data_sets: Dictionary of data sets to analyze
            
        Returns:
            Dictionary mapping data set names to detected types
        """
        detected_types = {}
        
        for name, values in data_sets.items():
            detected_type = self._detect_data_type(name, values)
            detected_types[name] = detected_type
        
        return detected_types
    
    def suggest_templates(self, data_sets: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """
        Suggest templates based on available data
        
        Args:
            data_sets: Available data sets
            
        Returns:
            List of suggested templates with match scores
        """
        suggestions = []
        data_types = self.detect_data_types(data_sets)
        
        # Location + Service pattern
        if any(t == "location" for t in data_types.values()) and \
           any(t == "service" for t in data_types.values()):
            suggestions.append({
                "template_id": "location_service",
                "name": "Location + Service Template",
                "pattern": "{location} {service}",
                "match_score": 0.95,
                "estimated_pages": self._calculate_combinations(data_sets, ["location", "service"]),
                "data_requirements": ["location", "service"],
                "benefits": ["Local SEO optimization", "High search intent", "Clear user need"]
            })
        
        # Product comparison pattern
        products = [name for name, dtype in data_types.items() if dtype == "product"]
        if len(products) >= 2:
            suggestions.append({
                "template_id": "comparison",
                "name": "Product Comparison Template",
                "pattern": "{product1} vs {product2}",
                "match_score": 0.90,
                "estimated_pages": self._calculate_combinations(data_sets, products[:2]),
                "data_requirements": products[:2],
                "benefits": ["High commercial intent", "Decision-stage content", "Natural linking"]
            })
        
        # Industry/Use-case pattern
        if any(t == "industry" for t in data_types.values()) and \
           any(t == "product" for t in data_types.values()):
            suggestions.append({
                "template_id": "industry_solution",
                "name": "Industry Solution Template",
                "pattern": "{product} for {industry}",
                "match_score": 0.85,
                "estimated_pages": self._calculate_combinations(data_sets, ["product", "industry"]),
                "data_requirements": ["product", "industry"],
                "benefits": ["Niche targeting", "B2B focus", "Industry-specific keywords"]
            })
        
        # How-to pattern
        if any(t == "action" for t in data_types.values()) and \
           any(t in ["product", "topic"] for t in data_types.values()):
            suggestions.append({
                "template_id": "how_to",
                "name": "How-To Guide Template",
                "pattern": "how to {action} {topic}",
                "match_score": 0.80,
                "estimated_pages": self._calculate_combinations(data_sets, ["action", "topic"]),
                "data_requirements": ["action", "topic"],
                "benefits": ["Informational intent", "Evergreen content", "Featured snippets"]
            })
        
        # Sort by match score
        suggestions.sort(key=lambda x: x["match_score"], reverse=True)
        
        return suggestions
    
    def generate_combinations(
        self,
        template_pattern: str,
        data_mapping: Dict[str, str],
        limit: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """
        Generate all possible combinations for a template
        
        Args:
            template_pattern: Template with {variables}
            data_mapping: Mapping of variable names to data set names
            limit: Optional limit on combinations
            
        Returns:
            List of variable combinations
        """
        # Extract variables from pattern
        variables = re.findall(r'\{(\w+)\}', template_pattern)
        
        # Get data for each variable
        data_lists = []
        for var in variables:
            data_set_name = data_mapping.get(var, var)
            if data_set_name in self.data_sets:
                data_lists.append(self.data_sets[data_set_name])
            else:
                return []  # Missing required data
        
        # Generate combinations
        combinations = []
        for combo in itertools.product(*data_lists):
            combination = dict(zip(variables, combo))
            combinations.append(combination)
            
            if limit and len(combinations) >= limit:
                break
        
        return combinations
    
    def estimate_page_count(
        self,
        template_pattern: str,
        data_mapping: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Calculate how many pages will be generated
        
        Args:
            template_pattern: Template pattern
            data_mapping: Variable to data set mapping
            
        Returns:
            Estimation details
        """
        variables = re.findall(r'\{(\w+)\}', template_pattern)
        
        counts = {}
        total = 1
        missing = []
        
        for var in variables:
            data_set_name = data_mapping.get(var, var)
            if data_set_name in self.data_sets:
                count = len(self.data_sets[data_set_name])
                counts[var] = count
                total *= count
            else:
                missing.append(var)
        
        if missing:
            return {
                "error": f"Missing data for variables: {', '.join(missing)}",
                "available_data": list(self.data_sets.keys())
            }
        
        return {
            "total_pages": total,
            "variable_counts": counts,
            "calculation": " × ".join([f"{var}({count})" for var, count in counts.items()]),
            "warnings": self._get_scale_warnings(total)
        }
    
    def merge_data_sets(
        self,
        source_sets: List[str],
        target_name: str,
        merge_type: str = "union"
    ) -> Dict[str, Any]:
        """
        Merge multiple data sets
        
        Args:
            source_sets: Names of sets to merge
            target_name: Name for merged set
            merge_type: "union" or "intersection"
            
        Returns:
            Merge results
        """
        if not all(name in self.data_sets for name in source_sets):
            missing = [name for name in source_sets if name not in self.data_sets]
            return {
                "success": False,
                "error": f"Data sets not found: {', '.join(missing)}"
            }
        
        if merge_type == "union":
            # Combine all unique values
            merged = set()
            for name in source_sets:
                merged.update(self.data_sets[name])
            merged_list = sorted(list(merged))
        else:  # intersection
            # Only keep common values
            merged = set(self.data_sets[source_sets[0]])
            for name in source_sets[1:]:
                merged = merged.intersection(set(self.data_sets[name]))
            merged_list = sorted(list(merged))
        
        # Store merged set
        self.data_sets[target_name] = merged_list
        
        # Generate statistics
        statistics = {
            "source_sets": source_sets,
            "merge_type": merge_type,
            "source_counts": {name: len(self.data_sets[name]) for name in source_sets},
            "merged_count": len(merged_list),
            "unique_values": len(set(merged_list))
        }
        
        self.data_statistics[target_name] = statistics
        
        return {
            "success": True,
            "merged_set": target_name,
            "statistics": statistics,
            "sample": merged_list[:10] if merged_list else []
        }
    
    def enrich_data(
        self,
        data_set_name: str,
        enrichment_type: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enrich data with variations, synonyms, or related terms
        
        Args:
            data_set_name: Name of data set to enrich
            enrichment_type: Type of enrichment (variations, synonyms, related)
            options: Enrichment options
            
        Returns:
            Enrichment results
        """
        if data_set_name not in self.data_sets:
            return {"success": False, "error": "Data set not found"}
        
        original_data = self.data_sets[data_set_name]
        enriched_data = []
        
        if enrichment_type == "variations":
            # Add variations (plurals, different cases, common misspellings)
            for value in original_data:
                enriched_data.append(value)
                
                # Add plural/singular
                if value.endswith('s'):
                    enriched_data.append(value[:-1])
                else:
                    enriched_data.append(value + 's')
                
                # Add with/without "the"
                if value.lower().startswith('the '):
                    enriched_data.append(value[4:])
                else:
                    enriched_data.append('The ' + value)
                
                # Add common variations
                if options and 'custom_variations' in options:
                    for variation_pattern in options['custom_variations']:
                        enriched_data.append(variation_pattern.format(value=value))
        
        elif enrichment_type == "location_modifiers":
            # Add location modifiers (near me, in my area, etc.)
            modifiers = options.get('modifiers', [
                "near me", "in my area", "nearby", "local", "around me"
            ])
            for value in original_data:
                enriched_data.append(value)
                for modifier in modifiers:
                    enriched_data.append(f"{value} {modifier}")
        
        elif enrichment_type == "year_variations":
            # Add year variations
            current_year = datetime.now().year
            years = options.get('years', [current_year, current_year + 1])
            for value in original_data:
                enriched_data.append(value)
                for year in years:
                    enriched_data.append(f"{value} {year}")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_enriched = []
        for item in enriched_data:
            if item.lower() not in seen:
                seen.add(item.lower())
                unique_enriched.append(item)
        
        # Create new enriched data set
        enriched_name = f"{data_set_name}_enriched"
        self.data_sets[enriched_name] = unique_enriched
        
        return {
            "success": True,
            "original_count": len(original_data),
            "enriched_count": len(unique_enriched),
            "enrichment_factor": len(unique_enriched) / len(original_data),
            "enriched_set_name": enriched_name,
            "sample": unique_enriched[:10]
        }
    
    def get_data_quality_report(
        self,
        data_set_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive data quality report
        
        Args:
            data_set_name: Optional specific data set, otherwise all
            
        Returns:
            Quality report with recommendations
        """
        if data_set_name:
            if data_set_name not in self.data_sets:
                return {"error": "Data set not found"}
            data_sets_to_check = {data_set_name: self.data_sets[data_set_name]}
        else:
            data_sets_to_check = self.data_sets
        
        report = {
            "summary": {},
            "details": {},
            "recommendations": []
        }
        
        total_values = 0
        total_unique = 0
        quality_scores = []
        
        for name, values in data_sets_to_check.items():
            # Analyze data quality
            analysis = self._analyze_data_quality(values)
            
            report["details"][name] = analysis
            total_values += len(values)
            total_unique += analysis["unique_count"]
            quality_scores.append(analysis["quality_score"])
            
            # Generate recommendations
            if analysis["duplicate_rate"] > 0.1:
                report["recommendations"].append({
                    "data_set": name,
                    "issue": "High duplicate rate",
                    "recommendation": f"Remove {analysis['duplicates']} duplicate values to improve quality"
                })
            
            if analysis["avg_length"] > 50:
                report["recommendations"].append({
                    "data_set": name,
                    "issue": "Long values detected",
                    "recommendation": "Consider shortening values for better URLs and readability"
                })
            
            if analysis["special_char_rate"] > 0.2:
                report["recommendations"].append({
                    "data_set": name,
                    "issue": "High special character usage",
                    "recommendation": "Clean special characters for better SEO compatibility"
                })
        
        # Overall summary
        report["summary"] = {
            "total_data_sets": len(data_sets_to_check),
            "total_values": total_values,
            "total_unique_values": total_unique,
            "average_quality_score": sum(quality_scores) / len(quality_scores) if quality_scores else 0,
            "overall_health": self._get_health_status(sum(quality_scores) / len(quality_scores) if quality_scores else 0)
        }
        
        return report
    
    def export_data(
        self,
        data_set_names: Optional[List[str]] = None,
        format: str = "csv",
        include_stats: bool = True
    ) -> Dict[str, Any]:
        """
        Export cleaned data in various formats
        
        Args:
            data_set_names: Specific sets to export (all if None)
            format: Export format (csv, json, tsv)
            include_stats: Include statistics in export
            
        Returns:
            Export data
        """
        if data_set_names:
            export_sets = {name: self.data_sets[name] 
                          for name in data_set_names 
                          if name in self.data_sets}
        else:
            export_sets = self.data_sets
        
        if format == "json":
            export_data = {
                "data_sets": export_sets,
                "metadata": {
                    "exported_at": datetime.now().isoformat(),
                    "total_sets": len(export_sets),
                    "total_values": sum(len(v) for v in export_sets.values())
                }
            }
            if include_stats:
                export_data["statistics"] = self.data_statistics
            
            return {
                "success": True,
                "format": "json",
                "data": export_data
            }
        
        elif format in ["csv", "tsv"]:
            # Convert to DataFrame for CSV/TSV export
            delimiter = "," if format == "csv" else "\t"
            
            # Find max length for padding
            max_len = max(len(values) for values in export_sets.values()) if export_sets else 0
            
            # Pad lists to same length
            padded_data = {}
            for name, values in export_sets.items():
                padded_values = values + [''] * (max_len - len(values))
                padded_data[name] = padded_values
            
            df = pd.DataFrame(padded_data)
            
            return {
                "success": True,
                "format": format,
                "data": df,
                "delimiter": delimiter
            }
        
        else:
            return {
                "success": False,
                "error": f"Unsupported format: {format}"
            }
    
    def list_data_sets(self) -> List[Dict[str, Any]]:
        """List all available data sets with metadata"""
        data_sets_info = []
        
        for name, values in self.data_sets.items():
            info = {
                "name": name,
                "count": len(values),
                "unique_count": len(set(values)),
                "data_type": self._detect_data_type(name, values),
                "sample": values[:5] if values else [],
                "statistics": self.data_statistics.get(name, {})
            }
            data_sets_info.append(info)
        
        return data_sets_info
    
    def clear_data_set(self, data_set_name: str) -> Dict[str, Any]:
        """Remove a data set"""
        if data_set_name not in self.data_sets:
            return {"success": False, "error": "Data set not found"}
        
        del self.data_sets[data_set_name]
        if data_set_name in self.data_statistics:
            del self.data_statistics[data_set_name]
        
        return {"success": True, "message": f"Data set '{data_set_name}' removed"}
    
    # Helper methods
    
    def _detect_encoding(self, file_path: str) -> str:
        """Detect file encoding"""
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding'] or 'utf-8'
    
    def _analyze_columns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze DataFrame columns to detect types"""
        analysis = {}
        
        for column in df.columns:
            values = df[column].dropna().astype(str).tolist()
            
            analysis[column] = {
                "original_name": column,
                "clean_name": self._clean_column_name(column),
                "row_count": len(values),
                "unique_count": len(set(values)),
                "suggested_type": self._detect_data_type(column, values),
                "sample_values": values[:5] if values else []
            }
        
        return analysis
    
    def _clean_column_name(self, name: str) -> str:
        """Clean column name for use as variable"""
        # Convert to lowercase and replace spaces/special chars with underscore
        clean = re.sub(r'[^a-zA-Z0-9]+', '_', name.lower())
        # Remove leading/trailing underscores
        clean = clean.strip('_')
        # Ensure it doesn't start with a number
        if clean and clean[0].isdigit():
            clean = 'col_' + clean
        return clean or 'column'
    
    def _detect_data_type(self, name: str, values: List[str]) -> str:
        """Detect the type of data based on name and values"""
        name_lower = name.lower()
        
        # Check name patterns
        if any(loc in name_lower for loc in ['location', 'city', 'region', 'area', 'place', 'country', 'state']):
            return "location"
        elif any(svc in name_lower for svc in ['service', 'offering', 'solution']):
            return "service"
        elif any(prod in name_lower for prod in ['product', 'item', 'tool', 'software']):
            return "product"
        elif any(ind in name_lower for ind in ['industry', 'sector', 'vertical', 'niche']):
            return "industry"
        elif any(act in name_lower for act in ['action', 'verb', 'do', 'perform']):
            return "action"
        elif any(topic in name_lower for topic in ['topic', 'subject', 'theme']):
            return "topic"
        
        # Check value patterns
        sample_values = values[:20] if len(values) > 20 else values
        
        # Location patterns
        if any(any(pattern in str(v).lower() for pattern in ['city', 'county', 'state'])
               for v in sample_values):
            return "location"
        
        # Service patterns
        if any(any(pattern in str(v).lower() for pattern in ['service', 'repair', 'installation', 'consulting'])
               for v in sample_values):
            return "service"
        
        # Default to generic
        return "generic"
    
    def _normalize_value(self, value: str) -> str:
        """Normalize value for consistency"""
        # Remove extra whitespace
        normalized = ' '.join(value.split())
        
        # Normalize unicode characters
        normalized = unicodedata.normalize('NFKD', normalized)
        
        # Title case for proper formatting
        # But preserve acronyms and special cases
        words = normalized.split()
        normalized_words = []
        
        for word in words:
            if word.isupper() and len(word) > 1:
                # Keep acronyms as-is
                normalized_words.append(word)
            elif word.lower() in ['and', 'or', 'the', 'in', 'of', 'for', 'to', 'with']:
                # Keep common words lowercase
                normalized_words.append(word.lower())
            else:
                # Title case for regular words
                normalized_words.append(word.capitalize())
        
        return ' '.join(normalized_words)
    
    def _clean_special_chars(self, value: str) -> str:
        """Clean special characters while preserving meaning"""
        # Replace common special chars with acceptable alternatives
        replacements = {
            '&': 'and',
            '@': 'at',
            '#': 'number',
            '%': 'percent',
            '+': 'plus',
            '=': 'equals',
            '*': '',
            '|': 'or',
            '~': '',
            '^': '',
            '<': 'less than',
            '>': 'greater than'
        }
        
        cleaned = value
        for char, replacement in replacements.items():
            cleaned = cleaned.replace(char, replacement)
        
        # Remove any remaining special characters except allowed ones
        cleaned = re.sub(r'[^a-zA-Z0-9\s\-,\.\'&\(\)/]', '', cleaned)
        
        # Clean up extra spaces
        cleaned = ' '.join(cleaned.split())
        
        return cleaned
    
    def _store_data(self, data: Dict[str, List[str]]) -> None:
        """Store imported data in internal storage"""
        for name, values in data.items():
            self.data_sets[name] = values
            self.data_statistics[name] = {
                "count": len(values),
                "unique_count": len(set(values)),
                "imported_at": datetime.now().isoformat()
            }
    
    def _generate_import_statistics(
        self,
        imported_data: Dict[str, List[str]],
        validation_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate statistics for imported data"""
        total_values = sum(len(values) for values in imported_data.values())
        total_unique = sum(len(set(values)) for values in imported_data.values())
        
        stats = {
            "total_columns": len(imported_data),
            "total_values": total_values,
            "total_unique_values": total_unique,
            "average_values_per_column": total_values / len(imported_data) if imported_data else 0,
            "columns": {}
        }
        
        for name, values in imported_data.items():
            stats["columns"][name] = {
                "count": len(values),
                "unique": len(set(values)),
                "validation": validation_results.get(name, {})
            }
        
        return stats
    
    def _generate_warnings(self, issues: Dict[str, Any]) -> List[str]:
        """Generate user-friendly warnings from validation issues"""
        warnings = []
        
        if issues["duplicates"]:
            warnings.append(f"Found {len(issues['duplicates'])} duplicate values that were removed")
        
        if issues["invalid_chars"]:
            warnings.append(f"{len(issues['invalid_chars'])} values contained invalid characters and were skipped")
        
        if issues["too_long"]:
            warnings.append(f"{len(issues['too_long'])} values were truncated due to length")
        
        if issues["too_short"]:
            warnings.append(f"{len(issues['too_short'])} values were too short and skipped")
        
        if issues["empty"] > 0:
            warnings.append(f"Skipped {issues['empty']} empty values")
        
        if issues["special_chars_removed"]:
            warnings.append(f"Cleaned special characters from {len(issues['special_chars_removed'])} values")
        
        return warnings
    
    def _calculate_quality_score(
        self,
        original_count: int,
        cleaned_count: int,
        issues: Dict[str, Any]
    ) -> float:
        """Calculate data quality score (0-100)"""
        if original_count == 0:
            return 0.0
        
        # Base score from retention rate
        retention_rate = cleaned_count / original_count
        base_score = retention_rate * 70
        
        # Deduct for various issues
        issue_penalties = {
            "duplicates": len(issues["duplicates"]) / original_count * 10,
            "invalid_chars": len(issues["invalid_chars"]) / original_count * 15,
            "special_chars_removed": len(issues["special_chars_removed"]) / original_count * 5
        }
        
        total_penalty = sum(issue_penalties.values())
        
        # Add bonus for high unique rate
        if cleaned_count > 0:
            unique_rate = len(set([v.lower() for v in issues.get("cleaned_data", [])])) / cleaned_count
            unique_bonus = unique_rate * 30
        else:
            unique_bonus = 0
        
        score = base_score - total_penalty + unique_bonus
        return max(0, min(100, score))
    
    def _calculate_combinations(self, data_sets: Dict[str, List[str]], variables: List[str]) -> int:
        """Calculate number of combinations for given variables"""
        total = 1
        for var in variables:
            if var in data_sets:
                total *= len(data_sets[var])
        return total
    
    def _get_scale_warnings(self, total_pages: int) -> List[str]:
        """Generate warnings based on scale"""
        warnings = []
        
        if total_pages > 10000:
            warnings.append(f"Large scale: {total_pages:,} pages. Consider filtering or limiting data.")
        elif total_pages > 50000:
            warnings.append(f"Very large scale: {total_pages:,} pages. May require batch processing.")
        
        if total_pages < 10:
            warnings.append("Low page count. Consider adding more data for better SEO impact.")
        
        return warnings
    
    def _get_import_error_suggestions(self, error: str) -> List[str]:
        """Provide helpful suggestions for import errors"""
        suggestions = []
        
        if "encoding" in error.lower() or "decode" in error.lower():
            suggestions.append("Try specifying encoding: 'utf-8', 'latin-1', or 'cp1252'")
            suggestions.append("Save the file as UTF-8 in your spreadsheet application")
        
        if "not found" in error.lower():
            suggestions.append("Check the file path is correct")
            suggestions.append("Ensure the file exists and you have read permissions")
        
        if "parse" in error.lower():
            suggestions.append("Ensure the file is a valid CSV format")
            suggestions.append("Check for inconsistent delimiters or quotes")
        
        return suggestions
    
    def _flatten_dict(self, d: Dict, parent_key: str = '') -> Dict[str, List[str]]:
        """Flatten nested dictionary structure"""
        items = {}
        
        for k, v in d.items():
            new_key = f"{parent_key}_{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self._flatten_dict(v, new_key))
            elif isinstance(v, list):
                items[new_key] = [str(item) for item in v]
            else:
                items[new_key] = [str(v)]
        
        return items
    
    def _process_json_array(self, data: List[Dict]) -> Dict[str, List[str]]:
        """Process array of objects into columnar data"""
        if not data:
            return {}
        
        # Extract all unique keys
        all_keys = set()
        for item in data:
            if isinstance(item, dict):
                all_keys.update(item.keys())
        
        # Build columnar data
        result = {key: [] for key in all_keys}
        
        for item in data:
            if isinstance(item, dict):
                for key in all_keys:
                    value = item.get(key, '')
                    result[key].append(str(value))
        
        return result
    
    def _analyze_data_quality(self, values: List[str]) -> Dict[str, Any]:
        """Analyze quality metrics for a data set"""
        if not values:
            return {
                "quality_score": 0,
                "unique_count": 0,
                "duplicate_rate": 0,
                "avg_length": 0,
                "special_char_rate": 0
            }
        
        # Calculate metrics
        unique_values = set(v.lower() for v in values)
        duplicate_count = len(values) - len(unique_values)
        
        lengths = [len(v) for v in values]
        avg_length = sum(lengths) / len(lengths)
        
        special_char_count = sum(1 for v in values if re.search(r'[^a-zA-Z0-9\s\-,\.\'&]', v))
        special_char_rate = special_char_count / len(values)
        
        # Calculate quality score
        quality_score = 100
        quality_score -= (duplicate_count / len(values)) * 20
        quality_score -= special_char_rate * 15
        if avg_length > 100:
            quality_score -= 10
        elif avg_length < 3:
            quality_score -= 15
        
        return {
            "quality_score": max(0, quality_score),
            "unique_count": len(unique_values),
            "duplicates": duplicate_count,
            "duplicate_rate": duplicate_count / len(values),
            "avg_length": avg_length,
            "min_length": min(lengths),
            "max_length": max(lengths),
            "special_char_rate": special_char_rate,
            "special_char_count": special_char_count
        }
    
    def _get_health_status(self, score: float) -> str:
        """Get health status from quality score"""
        if score >= 90:
            return "Excellent"
        elif score >= 75:
            return "Good"
        elif score >= 60:
            return "Fair"
        elif score >= 40:
            return "Poor"
        else:
            return "Critical"
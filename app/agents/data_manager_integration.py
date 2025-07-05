"""Integration module to connect Data Manager Agent with Template Builder and other components"""
from typing import Dict, List, Any, Optional, Tuple
from .data_manager import DataManagerAgent
from .template_builder import TemplateBuilderAgent
import logging

logger = logging.getLogger(__name__)

class DataManagerIntegration:
    """
    Integrates the Data Manager Agent with Template Builder and other system components
    to provide seamless data import, validation, and template matching.
    """
    
    def __init__(self):
        self.data_manager = DataManagerAgent()
        self.template_builder = TemplateBuilderAgent()
    
    def import_and_suggest_templates(
        self,
        file_path: str,
        file_type: str = "csv"
    ) -> Dict[str, Any]:
        """
        Import data and automatically suggest matching templates
        
        Args:
            file_path: Path to data file
            file_type: Type of file (csv, json)
            
        Returns:
            Import results with template suggestions
        """
        # Import data
        if file_type == "csv":
            import_result = self.data_manager.import_csv(file_path)
        elif file_type == "json":
            import_result = self.data_manager.import_json(file_path)
        else:
            return {"success": False, "error": f"Unsupported file type: {file_type}"}
        
        if not import_result["success"]:
            return import_result
        
        # Get template suggestions based on imported data
        template_suggestions = self.data_manager.suggest_templates(self.data_manager.data_sets)
        
        # Match with available templates in template builder
        matched_templates = []
        for suggestion in template_suggestions:
            template_id = suggestion["template_id"]
            template = self.template_builder.get_template(template_id)
            
            if template:
                # Validate data compatibility
                validation = self.template_builder.validate_data_for_template(
                    template_id=template_id,
                    data_sets=self.data_manager.data_sets
                )
                
                matched_templates.append({
                    "template": template,
                    "suggestion": suggestion,
                    "validation": validation,
                    "estimated_pages": suggestion["estimated_pages"]
                })
        
        return {
            "success": True,
            "import_result": import_result,
            "data_sets": self.data_manager.list_data_sets(),
            "template_suggestions": template_suggestions,
            "matched_templates": matched_templates
        }
    
    def prepare_data_for_template(
        self,
        template_id: str,
        data_mapping: Optional[Dict[str, str]] = None,
        enrichment_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Prepare and validate data for a specific template
        
        Args:
            template_id: Template to prepare data for
            data_mapping: Optional mapping of template variables to data sets
            enrichment_options: Optional data enrichment settings
            
        Returns:
            Prepared data with validation results
        """
        template = self.template_builder.get_template(template_id)
        if not template:
            return {"success": False, "error": "Template not found"}
        
        # Get required variables
        required_vars = template.get("required_variables", [])
        optional_vars = template.get("optional_variables", [])
        
        # Auto-map data sets to variables if not provided
        if not data_mapping:
            data_mapping = self._auto_map_data_to_variables(
                required_vars + optional_vars,
                self.data_manager.data_sets
            )
        
        # Validate data availability
        missing_data = []
        mapped_data = {}
        
        for var in required_vars:
            data_set_name = data_mapping.get(var)
            if not data_set_name or data_set_name not in self.data_manager.data_sets:
                missing_data.append(var)
            else:
                mapped_data[var] = self.data_manager.data_sets[data_set_name]
        
        if missing_data:
            return {
                "success": False,
                "error": f"Missing data for required variables: {', '.join(missing_data)}",
                "available_data": list(self.data_manager.data_sets.keys()),
                "required_variables": required_vars
            }
        
        # Apply enrichment if requested
        if enrichment_options:
            for var, options in enrichment_options.items():
                if var in mapped_data:
                    data_set_name = data_mapping[var]
                    enrichment_result = self.data_manager.enrich_data(
                        data_set_name=data_set_name,
                        enrichment_type=options["type"],
                        options=options.get("settings", {})
                    )
                    if enrichment_result["success"]:
                        # Update mapping to use enriched data
                        mapped_data[var] = self.data_manager.data_sets[enrichment_result["enriched_set_name"]]
        
        # Validate data with template
        validation = self.template_builder.validate_data_for_template(
            template_id=template_id,
            data_sets=mapped_data
        )
        
        # Generate quality report
        quality_report = self.data_manager.get_data_quality_report()
        
        # Estimate page generation
        estimation = self.template_builder.estimate_page_count(
            template_id=template_id,
            data_sets=mapped_data
        )
        
        return {
            "success": True,
            "template": template,
            "mapped_data": mapped_data,
            "data_mapping": data_mapping,
            "validation": validation,
            "quality_report": quality_report,
            "estimation": estimation
        }
    
    def generate_bulk_combinations(
        self,
        template_id: str,
        data_mapping: Dict[str, str],
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate all combinations for bulk page creation
        
        Args:
            template_id: Template to use
            data_mapping: Variable to data set mapping
            filters: Optional filters to apply
            limit: Maximum combinations to generate
            
        Returns:
            Generated combinations with metadata
        """
        template = self.template_builder.get_template(template_id)
        if not template:
            return {"success": False, "error": "Template not found"}
        
        # Generate combinations
        combinations = self.data_manager.generate_combinations(
            template_pattern=template["pattern"],
            data_mapping=data_mapping,
            limit=limit
        )
        
        # Apply filters if provided
        if filters:
            filtered_combinations = []
            for combo in combinations:
                include = True
                for var, filter_func in filters.items():
                    if var in combo and not filter_func(combo[var]):
                        include = False
                        break
                if include:
                    filtered_combinations.append(combo)
            combinations = filtered_combinations
        
        # Generate previews for first few combinations
        preview_count = min(5, len(combinations))
        previews = []
        
        for i in range(preview_count):
            preview = self.template_builder.generate_preview(
                template=template,
                sample_data=combinations[i]
            )
            previews.append(preview)
        
        return {
            "success": True,
            "template": template,
            "total_combinations": len(combinations),
            "combinations": combinations,
            "previews": previews,
            "data_mapping": data_mapping
        }
    
    def analyze_data_coverage(
        self,
        template_id: str
    ) -> Dict[str, Any]:
        """
        Analyze how well current data covers template requirements
        
        Args:
            template_id: Template to analyze against
            
        Returns:
            Coverage analysis with recommendations
        """
        template = self.template_builder.get_template(template_id)
        if not template:
            return {"success": False, "error": "Template not found"}
        
        required_vars = template.get("required_variables", [])
        optional_vars = template.get("optional_variables", [])
        all_vars = required_vars + optional_vars
        
        # Analyze coverage
        coverage = {
            "required": {},
            "optional": {},
            "missing": [],
            "recommendations": []
        }
        
        # Check each variable
        for var in required_vars:
            matched_sets = self._find_matching_data_sets(var)
            if matched_sets:
                best_match = matched_sets[0]
                coverage["required"][var] = {
                    "matched_set": best_match["name"],
                    "confidence": best_match["confidence"],
                    "value_count": len(self.data_manager.data_sets[best_match["name"]])
                }
            else:
                coverage["missing"].append(var)
                coverage["recommendations"].append(
                    f"Import or add data for '{var}' to use this template"
                )
        
        for var in optional_vars:
            matched_sets = self._find_matching_data_sets(var)
            if matched_sets:
                best_match = matched_sets[0]
                coverage["optional"][var] = {
                    "matched_set": best_match["name"],
                    "confidence": best_match["confidence"],
                    "value_count": len(self.data_manager.data_sets[best_match["name"]])
                }
        
        # Calculate coverage score
        required_coverage = len(coverage["required"]) / len(required_vars) if required_vars else 1.0
        optional_coverage = len(coverage["optional"]) / len(optional_vars) if optional_vars else 1.0
        
        coverage["score"] = {
            "required": required_coverage * 100,
            "optional": optional_coverage * 100,
            "overall": (required_coverage * 0.8 + optional_coverage * 0.2) * 100
        }
        
        # Add recommendations based on coverage
        if coverage["score"]["required"] < 100:
            coverage["recommendations"].append(
                "Add missing required data to fully utilize this template"
            )
        
        if coverage["score"]["optional"] < 50:
            coverage["recommendations"].append(
                "Consider adding optional data for more content variations"
            )
        
        return {
            "success": True,
            "template": template,
            "coverage": coverage,
            "available_data_sets": self.data_manager.list_data_sets()
        }
    
    def merge_and_prepare_data(
        self,
        merge_operations: List[Dict[str, Any]],
        target_template: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform data merge operations and prepare for template use
        
        Args:
            merge_operations: List of merge operations to perform
            target_template: Optional template to validate against
            
        Returns:
            Merge results with validation
        """
        results = {
            "merges": [],
            "final_data_sets": {},
            "validation": None
        }
        
        # Perform each merge operation
        for operation in merge_operations:
            merge_result = self.data_manager.merge_data_sets(
                source_sets=operation["sources"],
                target_name=operation["target"],
                merge_type=operation.get("type", "union")
            )
            results["merges"].append(merge_result)
        
        # Get final data sets
        results["final_data_sets"] = self.data_manager.list_data_sets()
        
        # Validate against template if provided
        if target_template:
            template = self.template_builder.get_template(target_template)
            if template:
                validation = self.template_builder.validate_data_for_template(
                    template_id=target_template,
                    data_sets=self.data_manager.data_sets
                )
                results["validation"] = validation
                
                # Estimate final page count
                estimation = self.template_builder.estimate_page_count(
                    template_id=target_template,
                    data_sets=self.data_manager.data_sets
                )
                results["estimation"] = estimation
        
        return results
    
    def export_prepared_data(
        self,
        template_id: str,
        format: str = "csv",
        include_combinations: bool = False,
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Export data prepared for a specific template
        
        Args:
            template_id: Template the data is prepared for
            format: Export format
            include_combinations: Include generated combinations
            limit: Limit combinations if included
            
        Returns:
            Export data
        """
        template = self.template_builder.get_template(template_id)
        if not template:
            return {"success": False, "error": "Template not found"}
        
        # Get base data export
        export_result = self.data_manager.export_data(
            format=format,
            include_stats=True
        )
        
        if not export_result["success"]:
            return export_result
        
        # Add template information
        export_result["template_info"] = {
            "id": template_id,
            "name": template["name"],
            "pattern": template["pattern"],
            "variables": template["variables"]
        }
        
        # Include combinations if requested
        if include_combinations:
            combinations = self.data_manager.generate_combinations(
                template_pattern=template["pattern"],
                data_mapping={var: var for var in template["variables"]},
                limit=limit
            )
            
            if format == "json":
                export_result["data"]["combinations"] = combinations
            elif format in ["csv", "tsv"]:
                # Convert combinations to DataFrame format
                import pandas as pd
                if combinations:
                    combo_df = pd.DataFrame(combinations)
                    export_result["combinations_data"] = combo_df
        
        return export_result
    
    # Helper methods
    
    def _auto_map_data_to_variables(
        self,
        variables: List[str],
        available_data: Dict[str, List[str]]
    ) -> Dict[str, str]:
        """Automatically map data sets to template variables"""
        mapping = {}
        
        for var in variables:
            matches = self._find_matching_data_sets(var)
            if matches:
                mapping[var] = matches[0]["name"]
        
        return mapping
    
    def _find_matching_data_sets(self, variable_name: str) -> List[Dict[str, Any]]:
        """Find data sets that match a variable name"""
        matches = []
        var_lower = variable_name.lower()
        
        for data_set_name in self.data_manager.data_sets:
            set_lower = data_set_name.lower()
            
            # Direct match
            if var_lower == set_lower:
                matches.append({"name": data_set_name, "confidence": 1.0})
            # Contains match
            elif var_lower in set_lower or set_lower in var_lower:
                matches.append({"name": data_set_name, "confidence": 0.8})
            # Partial match
            elif any(part in set_lower for part in var_lower.split('_')):
                matches.append({"name": data_set_name, "confidence": 0.6})
        
        # Sort by confidence
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        
        return matches
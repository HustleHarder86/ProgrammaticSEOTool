"""Variable Generator Agent - Uses AI to generate relevant variables based on business context and template patterns"""
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import re

from ai_client import AIClient

logger = logging.getLogger(__name__)

class VariableGeneratorAgent:
    """
    Agent responsible for generating relevant variables for programmatic SEO templates
    using AI based on business context and template patterns.
    """
    
    def __init__(self):
        """Initialize the Variable Generator Agent"""
        self.ai_client = AIClient()
        self.variable_patterns = {
            'location': ['city', 'state', 'country', 'region', 'area', 'neighborhood'],
            'category': ['type', 'category', 'style', 'model', 'variant', 'option'],
            'feature': ['feature', 'benefit', 'capability', 'function', 'specification'],
            'audience': ['audience', 'demographic', 'user', 'customer', 'persona'],
            'comparison': ['brand', 'competitor', 'alternative', 'option'],
            'use_case': ['use_case', 'application', 'scenario', 'purpose'],
            'industry': ['industry', 'sector', 'vertical', 'niche', 'market'],
            'platform': ['platform', 'channel', 'medium', 'network'],
            'time': ['year', 'season', 'month', 'period', 'timeline']
        }
    
    async def generate_variables(
        self,
        template_pattern: str,
        business_context: Dict[str, Any],
        additional_context: Optional[str] = None,
        target_count: int = 25
    ) -> Dict[str, Any]:
        """
        Generate relevant variables based on template and business context
        
        Args:
            template_pattern: The template pattern with {variable} placeholders
            business_context: Business analysis data from step 1
            additional_context: Optional user-provided context
            target_count: Target number of variable values to generate
            
        Returns:
            Dictionary containing generated variables and titles
        """
        try:
            # Extract variables from template pattern
            variables = self._extract_variables(template_pattern)
            
            if not variables:
                raise ValueError("No variables found in template pattern")
            
            # Detect variable types
            variable_types = self._detect_variable_types(variables)
            
            # Generate values for each variable
            variable_values = {}
            for var_name, var_type in variable_types.items():
                values = await self._generate_variable_values(
                    var_name,
                    var_type,
                    business_context,
                    additional_context,
                    target_count
                )
                variable_values[var_name] = values
            
            # Generate all possible combinations
            all_titles = self._generate_all_titles(template_pattern, variable_values)
            
            return {
                "variables": variable_values,
                "titles": all_titles,
                "total_count": len(all_titles),
                "template_pattern": template_pattern,
                "variable_types": variable_types
            }
            
        except Exception as e:
            logger.error(f"Error generating variables: {str(e)}")
            raise
    
    def _extract_variables(self, template_pattern: str) -> List[str]:
        """Extract variable names from template pattern"""
        # Match {variable} or [variable] patterns
        matches = re.findall(r'\{([^}]+)\}|\[([^\]]+)\]', template_pattern)
        variables = []
        for match in matches:
            var = match[0] if match[0] else match[1]
            if var and var not in variables:
                variables.append(var)
        return variables
    
    def _detect_variable_types(self, variables: List[str]) -> Dict[str, str]:
        """Detect the type of each variable based on name patterns"""
        variable_types = {}
        
        for var in variables:
            var_lower = var.lower()
            detected_type = 'generic'
            
            # Check against known patterns
            for pattern_type, patterns in self.variable_patterns.items():
                if any(pattern in var_lower for pattern in patterns):
                    detected_type = pattern_type
                    break
            
            variable_types[var] = detected_type
        
        return variable_types
    
    async def _generate_variable_values(
        self,
        variable_name: str,
        variable_type: str,
        business_context: Dict[str, Any],
        additional_context: Optional[str],
        target_count: int
    ) -> List[str]:
        """Generate values for a specific variable using AI"""
        
        # Build context-aware prompt
        prompt = self._build_generation_prompt(
            variable_name,
            variable_type,
            business_context,
            additional_context,
            target_count
        )
        
        # Generate values using AI
        response = await self.ai_client.generate(
            prompt,
            temperature=0.7,
            max_tokens=1000
        )
        
        # Parse and validate values
        values = self._parse_ai_response(response, variable_name)
        
        # Ensure we have the right amount
        if len(values) < target_count:
            # Generate more if needed
            additional_values = await self._generate_additional_values(
                variable_name,
                variable_type,
                business_context,
                values,
                target_count - len(values)
            )
            values.extend(additional_values)
        
        return values[:target_count]
    
    def _build_generation_prompt(
        self,
        variable_name: str,
        variable_type: str,
        business_context: Dict[str, Any],
        additional_context: Optional[str],
        target_count: int
    ) -> str:
        """Build AI prompt for generating variable values"""
        
        business_name = business_context.get('business_name', 'the business')
        business_desc = business_context.get('business_description', '')
        target_audience = business_context.get('target_audience', 'general audience')
        industry = business_context.get('industry', 'general')
        offerings = business_context.get('core_offerings', [])
        
        prompt = f"""Generate {target_count} relevant values for the variable "{variable_name}" in a programmatic SEO context.

Business Context:
- Business: {business_name}
- Description: {business_desc}
- Industry: {industry}
- Target Audience: {target_audience}
- Core Offerings: {', '.join(offerings) if offerings else 'Various services'}

Variable Type: {variable_type}
Variable Name: {variable_name}
"""

        if additional_context:
            prompt += f"\nAdditional Context: {additional_context}"
        
        # Add type-specific instructions
        if variable_type == 'location':
            prompt += f"""
Generate {target_count} relevant locations (cities, regions, etc.) that would be most relevant for {business_name}.
Consider the business's target market and likely service areas."""
        
        elif variable_type == 'category':
            prompt += f"""
Generate {target_count} relevant categories, types, or styles that relate to {business_name}'s offerings.
Focus on categories that users would actually search for."""
        
        elif variable_type == 'audience':
            prompt += f"""
Generate {target_count} specific audience segments or user types that would benefit from {business_name}'s services.
Be specific and use terms people would search for."""
        
        elif variable_type == 'platform':
            prompt += f"""
Generate {target_count} relevant platforms, channels, or networks related to {business_name}'s industry.
Focus on popular and searchable platforms."""
        
        elif variable_type == 'use_case':
            prompt += f"""
Generate {target_count} specific use cases or scenarios where {business_name}'s offerings would be valuable.
Use clear, searchable phrases."""
        
        else:
            prompt += f"""
Generate {target_count} relevant values that make sense for this variable in the context of {business_name}."""
        
        prompt += """

Requirements:
1. Return ONLY a JSON array of strings
2. Each value should be realistic and searchable
3. Values should be diverse but relevant
4. Use proper capitalization
5. Avoid duplicates
6. Focus on high-search-volume terms when possible

Example format: ["Value 1", "Value 2", "Value 3"]

Generate the values:"""
        
        return prompt
    
    def _parse_ai_response(self, response: str, variable_name: str) -> List[str]:
        """Parse AI response to extract variable values"""
        try:
            # Try to extract JSON from response
            # Handle responses that might have markdown code blocks
            if '```json' in response:
                json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
                if json_match:
                    response = json_match.group(1)
            elif '```' in response:
                code_match = re.search(r'```\s*(.*?)\s*```', response, re.DOTALL)
                if code_match:
                    response = code_match.group(1)
            
            # Try to parse as JSON
            values = json.loads(response.strip())
            
            if isinstance(values, list):
                # Clean and validate values
                cleaned_values = []
                for value in values:
                    if isinstance(value, str) and value.strip():
                        cleaned_values.append(value.strip())
                return cleaned_values
            else:
                logger.warning(f"AI response was not a list for {variable_name}")
                return []
                
        except json.JSONDecodeError:
            # Fallback: try to extract values from plain text
            logger.warning(f"Failed to parse JSON for {variable_name}, attempting text extraction")
            return self._extract_values_from_text(response)
    
    def _extract_values_from_text(self, text: str) -> List[str]:
        """Extract values from plain text response"""
        values = []
        
        # Try to find numbered or bulleted lists
        lines = text.strip().split('\n')
        for line in lines:
            # Remove common list markers
            cleaned = re.sub(r'^[\d\-\*\•\.]+\s*', '', line.strip())
            if cleaned and len(cleaned) > 2:
                # Remove quotes if present
                cleaned = cleaned.strip('"\'')
                if cleaned and cleaned not in values:
                    values.append(cleaned)
        
        return values
    
    async def _generate_additional_values(
        self,
        variable_name: str,
        variable_type: str,
        business_context: Dict[str, Any],
        existing_values: List[str],
        needed_count: int
    ) -> List[str]:
        """Generate additional values if initial generation was insufficient"""
        
        prompt = f"""Generate {needed_count} MORE values for "{variable_name}".

Already have: {', '.join(existing_values[:5])}...

Generate {needed_count} additional DIFFERENT values following the same pattern.
Return as JSON array.
"""
        
        response = await self.ai_client.generate(prompt, temperature=0.8)
        return self._parse_ai_response(response, variable_name)
    
    def _generate_all_titles(
        self,
        template_pattern: str,
        variable_values: Dict[str, List[str]]
    ) -> List[str]:
        """Generate all possible title combinations"""
        
        # Single variable case
        if len(variable_values) == 1:
            var_name = list(variable_values.keys())[0]
            titles = []
            for value in variable_values[var_name]:
                title = template_pattern.replace(f"{{{var_name}}}", value)
                title = title.replace(f"[{var_name}]", value)
                titles.append(title)
            return titles
        
        # Multiple variables case - generate all combinations
        titles = []
        variable_names = list(variable_values.keys())
        
        def generate_combinations(index: int, current_values: Dict[str, str]):
            if index == len(variable_names):
                # Generate title with current combination
                title = template_pattern
                for var_name, value in current_values.items():
                    title = title.replace(f"{{{var_name}}}", value)
                    title = title.replace(f"[{var_name}]", value)
                titles.append(title)
                return
            
            var_name = variable_names[index]
            for value in variable_values[var_name]:
                current_values[var_name] = value
                generate_combinations(index + 1, current_values)
        
        generate_combinations(0, {})
        return titles
    
    async def suggest_additional_templates(
        self,
        business_context: Dict[str, Any],
        current_template: str,
        generated_variables: Dict[str, List[str]]
    ) -> List[Dict[str, Any]]:
        """Suggest additional template patterns based on generated variables"""
        
        prompt = f"""Based on the following business and generated variables, suggest 3-5 additional programmatic SEO template patterns:

Business: {business_context.get('business_name')}
Current Template: {current_template}
Available Variables: {', '.join(generated_variables.keys())}

Suggest template patterns that:
1. Use the same variables in different combinations
2. Target different search intents
3. Would create valuable SEO pages

Return as JSON array with format:
[{{"pattern": "template pattern", "intent": "search intent", "example": "example title"}}]
"""
        
        response = await self.ai_client.generate(prompt, temperature=0.7)
        
        try:
            suggestions = json.loads(response)
            return suggestions
        except:
            return []
    
    def validate_generated_variables(
        self,
        variables: Dict[str, List[str]],
        min_values: int = 5
    ) -> Dict[str, Any]:
        """Validate that generated variables meet quality standards"""
        
        validation_results = {
            "is_valid": True,
            "warnings": [],
            "errors": []
        }
        
        for var_name, values in variables.items():
            # Check minimum count
            if len(values) < min_values:
                validation_results["warnings"].append(
                    f"Variable '{var_name}' has only {len(values)} values (minimum recommended: {min_values})"
                )
            
            # Check for duplicates
            unique_values = set(v.lower() for v in values)
            if len(unique_values) < len(values):
                validation_results["warnings"].append(
                    f"Variable '{var_name}' contains duplicate values"
                )
            
            # Check for empty or invalid values
            invalid_count = sum(1 for v in values if not v or len(v.strip()) < 2)
            if invalid_count > 0:
                validation_results["errors"].append(
                    f"Variable '{var_name}' contains {invalid_count} invalid values"
                )
                validation_results["is_valid"] = False
        
        return validation_results
"""Page generation engine for creating bulk pages from templates and data"""
import re
import itertools
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import hashlib
import json
from sqlalchemy.orm import Session

from models import Template, DataSet, GeneratedPage, Project
from content_variation import ContentVariationEngine, enhance_content_quality, ensure_minimum_quality


class PageGenerator:
    def __init__(self):
        self.variation_engine = ContentVariationEngine()
        
    def extract_variables_from_template(self, pattern: str) -> List[str]:
        """Extract variable names from a template pattern
        
        Args:
            pattern: Template pattern like "[City] [Service] Provider"
            
        Returns:
            List of variable names like ["City", "Service"]
        """
        # Find all variables in square brackets
        variables = re.findall(r'\[([^\]]+)\]', pattern)
        return variables
    
    def load_datasets_for_variables(self, project_id: str, template: Template, db: Session) -> Dict[str, List[Dict[str, Any]]]:
        """Load all datasets for a project and map to template variables
        
        Args:
            project_id: Project ID
            template: Template object with variables
            db: Database session
            
        Returns:
            Dict mapping variable names to their data lists
        """
        # Get all datasets for the project
        datasets = db.query(DataSet).filter(DataSet.project_id == project_id).all()
        
        if not datasets:
            return {}
        
        # Map variables to data
        variable_data = {}
        
        for variable in template.variables:
            variable_lower = variable.lower()
            
            # Try to find matching column in datasets
            for dataset in datasets:
                if dataset.data:
                    # Check columns in first row
                    first_row = dataset.data[0] if dataset.data else {}
                    
                    for column_name in first_row.keys():
                        if column_name.lower() == variable_lower:
                            # Extract this column's data
                            column_data = []
                            for row in dataset.data:
                                if column_name in row and row[column_name]:
                                    column_data.append({
                                        'value': row[column_name],
                                        'dataset_id': dataset.id,
                                        'dataset_name': dataset.name,
                                        # Include other columns as metadata
                                        'metadata': {k: v for k, v in row.items() if k != column_name}
                                    })
                            
                            if column_data:
                                variable_data[variable] = column_data
                                break
                    
                    if variable in variable_data:
                        break
        
        return variable_data
    
    def generate_all_combinations(self, variable_data: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Generate all possible combinations of variable values
        
        Args:
            variable_data: Dict mapping variables to their possible values
            
        Returns:
            List of combination dictionaries
        """
        if not variable_data:
            return []
        
        # Get variable names and their value lists
        variables = list(variable_data.keys())
        value_lists = [variable_data[var] for var in variables]
        
        # Generate all combinations
        combinations = []
        for combo in itertools.product(*value_lists):
            combination = {}
            for i, var in enumerate(variables):
                combination[var] = combo[i]
            combinations.append(combination)
        
        return combinations
    
    def replace_variables_in_content(self, content: str, variables: Dict[str, Dict[str, Any]]) -> str:
        """Replace variables in content with actual values
        
        Args:
            content: Content with [Variable] placeholders
            variables: Dict of variable values
            
        Returns:
            Content with variables replaced
        """
        result = content
        
        for var_name, var_data in variables.items():
            # Get the actual value
            value = var_data['value'] if isinstance(var_data, dict) else str(var_data)
            
            # Replace [Variable] with value
            result = result.replace(f'[{var_name}]', value)
            
            # Also replace lowercase version
            result = result.replace(f'[{var_name.lower()}]', value.lower())
            
            # Replace variations like {Variable} or {{Variable}}
            result = result.replace(f'{{{var_name}}}', value)
            result = result.replace(f'{{{{{var_name}}}}}', value)
        
        return result
    
    def generate_unique_content(self, template: Template, variables: Dict[str, Any], 
                              page_index: int, total_pages: int) -> Dict[str, Any]:
        """Generate unique content for a specific page
        
        Args:
            template: Template object
            variables: Variable values for this page
            page_index: Index of current page
            total_pages: Total number of pages being generated
            
        Returns:
            Dict with title, meta_description, content sections, etc.
        """
        # Get template sections
        template_sections = template.template_sections or {}
        seo_structure = template_sections.get('seo_structure', {})
        content_sections = template_sections.get('content_sections', [])
        
        # Create keyword from pattern
        keyword = self.replace_variables_in_content(template.pattern, variables)
        
        # Generate unique structure for this page
        unique_structure = self.variation_engine.generate_unique_structure(
            keyword, 
            'general'  # Could be enhanced to detect content type
        )
        
        # Generate base content sections
        generated_sections = []
        
        # Add introduction with variation
        intro_variation = self.variation_engine.intro_variations[
            page_index % len(self.variation_engine.intro_variations)
        ]
        intro = intro_variation.format(keyword=keyword)
        generated_sections.append({
            'type': 'introduction',
            'content': intro
        })
        
        # Process template content sections
        for i, section in enumerate(content_sections):
            section_content = self.replace_variables_in_content(
                section.get('content', ''),
                variables
            )
            
            # Add variation to section content
            if i == 0:  # First main section
                section_content = self.variation_engine.add_contextual_content(
                    section_content, keyword
                )
            
            generated_sections.append({
                'type': 'content',
                'heading': self.replace_variables_in_content(
                    section.get('heading', f'Section {i+1}'),
                    variables
                ),
                'content': section_content
            })
        
        # Add unique elements based on page index
        unique_elements = unique_structure['unique_elements']
        if 'faq' in unique_elements or page_index % 3 == 0:
            faq_content = self._generate_faq_section(keyword, variables)
            generated_sections.append({
                'type': 'faq',
                'heading': f'Frequently Asked Questions about {keyword}',
                'content': faq_content
            })
        
        if 'statistics_section' in unique_elements or page_index % 4 == 1:
            stats_content = self._generate_statistics_section(keyword, variables)
            generated_sections.append({
                'type': 'statistics',
                'heading': f'{keyword} by the Numbers',
                'content': stats_content
            })
        
        # Add conclusion with variation
        conclusion_variation = self.variation_engine.conclusion_variations[
            page_index % len(self.variation_engine.conclusion_variations)
        ]
        conclusion = conclusion_variation.format(
            keyword=keyword,
            benefit='business growth',
            action='implement these strategies',
            main_point='understanding the fundamentals'
        )
        generated_sections.append({
            'type': 'conclusion',
            'content': conclusion
        })
        
        # Generate SEO elements
        title = self.replace_variables_in_content(
            seo_structure.get('title_template', f'{template.pattern} | Professional Guide'),
            variables
        )
        
        meta_description = self.replace_variables_in_content(
            seo_structure.get('meta_description_template', 
                            f'Complete guide to {template.pattern}. Expert insights and practical tips.'),
            variables
        )
        
        h1 = self.replace_variables_in_content(
            seo_structure.get('h1_template', template.pattern),
            variables
        )
        
        # Generate URL slug
        slug = self._generate_url_slug(keyword)
        
        return {
            'title': title,
            'meta_description': meta_description,
            'h1': h1,
            'keyword': keyword,
            'slug': slug,
            'content_sections': generated_sections,
            'unique_elements': unique_elements,
            'variation_index': page_index,
            'total_variations': total_pages
        }
    
    def _generate_faq_section(self, keyword: str, variables: Dict[str, Any]) -> str:
        """Generate FAQ section content"""
        faq_templates = [
            {
                'q': f'What is {keyword}?',
                'a': f'{keyword} is a comprehensive solution that helps businesses improve their operations and achieve better results.'
            },
            {
                'q': f'How much does {keyword} cost?',
                'a': f'The cost of {keyword} varies depending on your specific needs and scale. Contact us for a customized quote.'
            },
            {
                'q': f'How long does it take to implement {keyword}?',
                'a': f'Implementation of {keyword} typically takes 2-4 weeks, depending on the complexity of your requirements.'
            },
            {
                'q': f'Do you offer support for {keyword}?',
                'a': f'Yes, we provide comprehensive support for {keyword} including training, documentation, and ongoing assistance.'
            }
        ]
        
        faq_content = ""
        for faq in faq_templates[:3]:  # Use 3 FAQs
            faq_content += f"**{faq['q']}**\n\n{faq['a']}\n\n"
        
        return faq_content
    
    def _generate_statistics_section(self, keyword: str, variables: Dict[str, Any]) -> str:
        """Generate statistics section with dynamic numbers"""
        import random
        
        stats = [
            f"- {random.randint(70, 95)}% of businesses report improved efficiency with {keyword}",
            f"- Average ROI of {random.randint(200, 500)}% within the first year",
            f"- {random.randint(40, 80)}% reduction in operational costs",
            f"- Customer satisfaction increases by {random.randint(25, 45)}%",
            f"- Implementation time reduced by {random.randint(30, 60)}%"
        ]
        
        return "\n".join(stats[:4])
    
    def _generate_url_slug(self, keyword: str) -> str:
        """Generate URL-friendly slug from keyword"""
        # Convert to lowercase and replace spaces with hyphens
        slug = keyword.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special characters
        slug = re.sub(r'[-\s]+', '-', slug)  # Replace spaces with hyphens
        slug = slug.strip('-')  # Remove leading/trailing hyphens
        
        return slug
    
    def generate_preview_pages(self, project_id: str, template_id: str, 
                             db: Session, limit: int = 5) -> List[Dict[str, Any]]:
        """Generate preview pages for a template
        
        Args:
            project_id: Project ID
            template_id: Template ID
            db: Database session
            limit: Number of preview pages to generate
            
        Returns:
            List of generated page previews
        """
        # Get template
        template = db.query(Template).filter(Template.id == template_id).first()
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # Load datasets
        variable_data = self.load_datasets_for_variables(project_id, template, db)
        
        if not variable_data:
            # Generate sample data if no data available
            sample_data = self._generate_sample_data(template.variables)
            variable_data = sample_data
        
        # Generate combinations
        all_combinations = self.generate_all_combinations(variable_data)
        
        # Limit combinations for preview
        preview_combinations = all_combinations[:limit]
        
        # Generate pages
        preview_pages = []
        for i, combination in enumerate(preview_combinations):
            page_content = self.generate_unique_content(
                template, combination, i, len(preview_combinations)
            )
            
            # Add combination data
            page_content['variables'] = combination
            page_content['preview_index'] = i + 1
            
            preview_pages.append(page_content)
        
        return preview_pages
    
    def _generate_sample_data(self, variables: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Generate sample data for preview when no data is available"""
        sample_values = {
            'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
            'service': ['Web Design', 'SEO', 'Digital Marketing', 'Content Creation', 'PPC Management'],
            'industry': ['Healthcare', 'Finance', 'Technology', 'Retail', 'Manufacturing'],
            'product': ['Software', 'Consulting', 'Training', 'Support', 'Integration'],
            'location': ['Downtown', 'North Side', 'South Side', 'East End', 'West End']
        }
        
        sample_data = {}
        for variable in variables:
            var_lower = variable.lower()
            
            # Try to match with sample values
            values = None
            for key, val_list in sample_values.items():
                if key in var_lower or var_lower in key:
                    values = val_list
                    break
            
            # Default values if no match
            if not values:
                values = [f'{variable} 1', f'{variable} 2', f'{variable} 3', 
                         f'{variable} 4', f'{variable} 5']
            
            sample_data[variable] = [
                {'value': val, 'dataset_id': 'sample', 'dataset_name': 'Sample Data', 'metadata': {}}
                for val in values
            ]
        
        return sample_data
    
    def generate_pages_from_variables(self, project_id: str, template_id: str,
                                     variables_data: Dict[str, List[str]], 
                                     selected_titles: Optional[List[str]],
                                     db: Session, batch_size: int = 100) -> Tuple[int, List[str]]:
        """Generate pages from AI-generated variables and selected titles
        
        Args:
            project_id: Project ID
            template_id: Template ID
            variables_data: Dict mapping variable names to their values
            selected_titles: Optional list of specific titles to generate
            db: Database session
            batch_size: Number of pages to process at once
            
        Returns:
            Tuple of (total_pages_generated, list_of_page_ids)
        """
        # Get template and project
        template = db.query(Template).filter(Template.id == template_id).first()
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        # Convert variables_data to the expected format
        variable_data = {}
        for var_name, values in variables_data.items():
            variable_data[var_name] = [
                {'value': val, 'dataset_id': 'ai_generated', 'dataset_name': 'AI Generated', 'metadata': {}}
                for val in values
            ]
        
        # Generate combinations
        all_combinations = self.generate_all_combinations(variable_data)
        
        # Filter combinations if specific titles are selected
        if selected_titles:
            print(f"DEBUG: Filtering combinations for {len(selected_titles)} selected titles")
            print(f"DEBUG: Template pattern: {template.pattern}")
            print(f"DEBUG: First 5 selected titles: {selected_titles[:5]}")
            
            filtered_combinations = []
            for combo in all_combinations:
                # Generate title from combination
                title = self._generate_title_from_combo(template.pattern, combo)
                if title in selected_titles:
                    filtered_combinations.append(combo)
            
            print(f"DEBUG: Filtered to {len(filtered_combinations)} combinations from {len(all_combinations)}")
            all_combinations = filtered_combinations
        
        total_combinations = len(all_combinations)
        if total_combinations == 0:
            return 0, []
        
        skipped_count = 0  # Track how many were skipped due to duplicates
        
        # Process pages (same as generate_all_pages from here)
        generated_page_ids = []
        
        for batch_start in range(0, total_combinations, batch_size):
            batch_end = min(batch_start + batch_size, total_combinations)
            batch_combinations = all_combinations[batch_start:batch_end]
            
            for i, combination in enumerate(batch_combinations):
                global_index = batch_start + i
                
                # Generate unique content
                page_content = self.generate_unique_content(
                    template, combination, global_index, total_combinations
                )
                
                # Create content hash to check for duplicates
                content_hash = self._generate_content_hash(page_content)
                
                # Check if page already exists
                existing_page = db.query(GeneratedPage).filter(
                    GeneratedPage.project_id == project_id,
                    GeneratedPage.template_id == template_id,
                    GeneratedPage.title == page_content['title']
                ).first()
                
                if not existing_page:
                    # Save generated page
                    generated_page = GeneratedPage(
                        project_id=project_id,
                        template_id=template_id,
                        title=page_content['title'],
                        content=page_content,
                        meta_data={
                            'keyword': page_content.get('keyword', ''),
                            'slug': page_content.get('slug', ''),
                            'variables': combination,
                            'seo_score': page_content.get('seo_score', 0),
                            'content_hash': content_hash,
                            'quality_score': page_content.get('quality_metrics', {}).get('quality_score', 0)
                        }
                    )
                    
                    db.add(generated_page)
                    db.flush()  # Flush to get the ID
                    generated_page_ids.append(generated_page.id)
                else:
                    skipped_count += 1
                    print(f"DEBUG: Skipped duplicate page: {page_content['title']}")
            
            # Commit batch
            db.commit()
        
        print(f"DEBUG: Page generation complete - Generated: {len(generated_page_ids)}, Skipped (duplicates): {skipped_count}")
        return len(generated_page_ids), generated_page_ids
    
    def _generate_title_from_combo(self, pattern: str, combination: Dict[str, Any]) -> str:
        """Generate title from pattern and combination"""
        title = pattern
        for var_name, var_data in combination.items():
            value = var_data['value'] if isinstance(var_data, dict) else var_data
            title = title.replace(f'[{var_name}]', str(value))
            title = title.replace(f'{{{var_name}}}', str(value))
        return title
    
    def generate_all_pages(self, project_id: str, template_id: str, 
                          db: Session, batch_size: int = 100) -> Tuple[int, List[str]]:
        """Generate all pages for a template
        
        Args:
            project_id: Project ID
            template_id: Template ID
            db: Database session
            batch_size: Number of pages to process at once
            
        Returns:
            Tuple of (total_pages_generated, list_of_page_ids)
        """
        # Get template and project
        template = db.query(Template).filter(Template.id == template_id).first()
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        # Load datasets
        variable_data = self.load_datasets_for_variables(project_id, template, db)
        
        if not variable_data:
            raise ValueError("No data available for template variables")
        
        # Generate all combinations
        all_combinations = self.generate_all_combinations(variable_data)
        total_combinations = len(all_combinations)
        
        if total_combinations == 0:
            return 0, []
        
        # Process in batches for efficiency
        generated_page_ids = []
        
        for batch_start in range(0, total_combinations, batch_size):
            batch_end = min(batch_start + batch_size, total_combinations)
            batch_combinations = all_combinations[batch_start:batch_end]
            
            # Generate pages for this batch
            for i, combination in enumerate(batch_combinations):
                global_index = batch_start + i
                
                # Generate unique content
                page_content = self.generate_unique_content(
                    template, combination, global_index, total_combinations
                )
                
                # Create content hash to check for duplicates
                content_hash = self._generate_content_hash(page_content)
                
                # Check if page already exists
                existing_page = db.query(GeneratedPage).filter(
                    GeneratedPage.project_id == project_id,
                    GeneratedPage.template_id == template_id,
                    GeneratedPage.meta_data.contains({'content_hash': content_hash})
                ).first()
                
                if not existing_page:
                    # Create GeneratedPage entry
                    generated_page = GeneratedPage(
                        project_id=project_id,
                        template_id=template_id,
                        title=page_content['title'],
                        content=page_content,
                        meta_data={
                            'content_hash': content_hash,
                            'variables': {k: v['value'] if isinstance(v, dict) else v 
                                        for k, v in combination.items()},
                            'slug': page_content['slug'],
                            'keyword': page_content['keyword'],
                            'generation_index': global_index
                        }
                    )
                    
                    db.add(generated_page)
                    db.flush()  # Flush to get the ID
                    generated_page_ids.append(generated_page.id)
            
            # Commit batch
            db.commit()
        
        return len(generated_page_ids), generated_page_ids
    
    def _generate_content_hash(self, content: Dict[str, Any]) -> str:
        """Generate hash of content for duplicate detection"""
        # Create a string representation of key content elements
        content_string = f"{content.get('title', '')}{content.get('keyword', '')}"
        
        # Add content sections
        for section in content.get('content_sections', []):
            content_string += section.get('content', '')
        
        # Generate hash
        return hashlib.md5(content_string.encode()).hexdigest()
    
    def get_generated_pages(self, project_id: str, template_id: Optional[str], 
                           db: Session, offset: int = 0, limit: int = 50) -> List[GeneratedPage]:
        """Get generated pages for a project/template
        
        Args:
            project_id: Project ID
            template_id: Optional template ID filter
            db: Database session
            offset: Pagination offset
            limit: Number of pages to return
            
        Returns:
            List of GeneratedPage objects
        """
        query = db.query(GeneratedPage).filter(GeneratedPage.project_id == project_id)
        
        if template_id:
            query = query.filter(GeneratedPage.template_id == template_id)
        
        pages = query.offset(offset).limit(limit).all()
        
        return pages
    
    def enhance_page_quality(self, page: GeneratedPage, project: Project, 
                           all_pages: List[GeneratedPage]) -> Dict[str, Any]:
        """Enhance page quality with internal linking and quality improvements
        
        Args:
            page: GeneratedPage object
            project: Project object
            all_pages: List of all generated pages for internal linking
            
        Returns:
            Enhanced content dict
        """
        # Get all keywords for internal linking
        all_keywords = [p.meta_data.get('keyword', '') for p in all_pages if p.id != page.id]
        
        # Get business info from project
        business_info = project.business_analysis or {
            'name': project.name,
            'industry': 'General'
        }
        
        # Enhance content sections
        enhanced_content = page.content.copy()
        
        # Combine all content sections into a single content string
        full_content = ""
        for section in enhanced_content.get('content_sections', []):
            if section.get('heading'):
                full_content += f"## {section['heading']}\n\n"
            full_content += section.get('content', '') + "\n\n"
        
        # Apply quality enhancements
        enhanced_full_content = enhance_content_quality(
            full_content,
            page.meta_data.get('keyword', ''),
            business_info,
            all_keywords=all_keywords
        )
        
        # Check quality metrics
        quality_metrics = ensure_minimum_quality(
            enhanced_full_content,
            page.meta_data.get('keyword', '')
        )
        
        # Update enhanced content
        enhanced_content['full_content'] = enhanced_full_content
        enhanced_content['quality_metrics'] = quality_metrics
        enhanced_content['internal_links_added'] = len(all_keywords[:8])  # Number of potential internal links
        
        return enhanced_content
"""API Usage Tracker for monitoring costs and usage"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

class UsageTracker:
    def __init__(self):
        self.usage_file = os.path.join(os.path.dirname(__file__), 'usage_data.json')
        self.load_usage_data()
        
        # Perplexity API actual pricing (as of 2024)
        # Complete pricing structure for all models
        self.models = {
            'sonar': {
                'name': 'Sonar (Standard)',
                'input_cost_per_1m': 1.0,  # $1 per million input tokens
                'output_cost_per_1m': 1.0,  # $1 per million output tokens
                'request_cost_low': 0.005,  # $5 per 1000 requests
                'request_cost_medium': 0.008,  # $8 per 1000 requests
                'request_cost_high': 0.012  # $12 per 1000 requests
            },
            'sonar-pro': {
                'name': 'Sonar Pro',
                'input_cost_per_1m': 3.0,  # $3 per million input tokens
                'output_cost_per_1m': 15.0,  # $15 per million output tokens
                'request_cost_low': 0.006,  # $6 per 1000 requests
                'request_cost_medium': 0.010,  # $10 per 1000 requests
                'request_cost_high': 0.014  # $14 per 1000 requests
            },
            'sonar-reasoning': {
                'name': 'Sonar Reasoning',
                'input_cost_per_1m': 1.0,  # $1 per million input tokens
                'output_cost_per_1m': 5.0,  # $5 per million output tokens
                'request_cost_low': 0.005,
                'request_cost_medium': 0.008,
                'request_cost_high': 0.012
            },
            'sonar-reasoning-pro': {
                'name': 'Sonar Reasoning Pro',
                'input_cost_per_1m': 2.0,  # $2 per million input tokens
                'output_cost_per_1m': 8.0,  # $8 per million output tokens
                'request_cost_low': 0.006,
                'request_cost_medium': 0.010,
                'request_cost_high': 0.014
            }
        }
        
        # Default model for calculations (can be changed by user)
        self.current_model = 'sonar'
        
        # Endpoint configurations with token estimates
        self.endpoints = {
            'analyze_business': {
                'input_tokens_avg': 250,
                'output_tokens_avg': 250,
                'request_complexity': 'low',  # low/medium/high affects request pricing
                'description': 'Business analysis with AI'
            },
            'generate_keywords': {
                'input_tokens_avg': 150,
                'output_tokens_avg': 150,
                'request_complexity': 'low',
                'description': 'Keyword generation'
            },
            'generate_keywords_seed': {
                'input_tokens_avg': 50,
                'output_tokens_avg': 50,
                'request_complexity': 'low',
                'description': 'Seed keyword suggestions'
            },
            'generate_content': {
                'input_tokens_avg': 500,
                'output_tokens_avg': 2000,
                'request_complexity': 'medium',
                'description': 'Content generation per article'
            }
        }
    
    def load_usage_data(self):
        """Load usage data from file"""
        try:
            with open(self.usage_file, 'r') as f:
                self.usage_data = json.load(f)
        except:
            self.usage_data = {
                'total_requests': 0,
                'total_cost': 0,
                'daily_usage': {},
                'endpoint_usage': {},
                'monthly_usage': {}
            }
    
    def save_usage_data(self):
        """Save usage data to file"""
        try:
            with open(self.usage_file, 'w') as f:
                json.dump(self.usage_data, f, indent=2)
        except Exception as e:
            print(f"Error saving usage data: {e}")
    
    def track_usage(self, endpoint: str, input_tokens: int = None, output_tokens: int = None, 
                   count: int = 1, model: str = None):
        """Track API usage for an endpoint with separate input/output tokens"""
        today = datetime.now().strftime('%Y-%m-%d')
        month = datetime.now().strftime('%Y-%m')
        
        # Use current model if not specified
        if model is None:
            model = self.current_model
            
        # Get endpoint config
        endpoint_config = self.endpoints.get(endpoint, {})
        
        # Use estimated tokens if not provided
        if input_tokens is None:
            input_tokens = endpoint_config.get('input_tokens_avg', 100) * count
        if output_tokens is None:
            output_tokens = endpoint_config.get('output_tokens_avg', 100) * count
            
        total_tokens = input_tokens + output_tokens
        
        # Calculate cost based on model and complexity
        cost = 0
        if model in self.models and endpoint in self.endpoints:
            model_pricing = self.models[model]
            complexity = endpoint_config.get('request_complexity', 'low')
            
            # Get request cost based on complexity
            request_cost_key = f'request_cost_{complexity}'
            request_cost = model_pricing.get(request_cost_key, 0.005)
            
            # Calculate total cost
            cost = request_cost * count  # Request fee
            cost += (input_tokens / 1_000_000) * model_pricing['input_cost_per_1m']  # Input tokens
            cost += (output_tokens / 1_000_000) * model_pricing['output_cost_per_1m']  # Output tokens
        
        # Update total stats
        self.usage_data['total_requests'] += count
        self.usage_data['total_cost'] += cost
        
        # Update daily usage
        if today not in self.usage_data['daily_usage']:
            self.usage_data['daily_usage'][today] = {
                'requests': 0,
                'cost': 0,
                'endpoints': {}
            }
        
        self.usage_data['daily_usage'][today]['requests'] += count
        self.usage_data['daily_usage'][today]['cost'] += cost
        
        if endpoint not in self.usage_data['daily_usage'][today]['endpoints']:
            self.usage_data['daily_usage'][today]['endpoints'][endpoint] = {
                'count': 0,
                'cost': 0,
                'tokens': 0,
                'input_tokens': 0,
                'output_tokens': 0,
                'model': model
            }
        
        self.usage_data['daily_usage'][today]['endpoints'][endpoint]['count'] += count
        self.usage_data['daily_usage'][today]['endpoints'][endpoint]['cost'] += cost
        self.usage_data['daily_usage'][today]['endpoints'][endpoint]['tokens'] += total_tokens
        self.usage_data['daily_usage'][today]['endpoints'][endpoint]['input_tokens'] += input_tokens
        self.usage_data['daily_usage'][today]['endpoints'][endpoint]['output_tokens'] += output_tokens
        self.usage_data['daily_usage'][today]['endpoints'][endpoint]['model'] = model
        
        # Update monthly usage
        if month not in self.usage_data['monthly_usage']:
            self.usage_data['monthly_usage'][month] = {
                'requests': 0,
                'cost': 0,
                'endpoints': {}
            }
        
        self.usage_data['monthly_usage'][month]['requests'] += count
        self.usage_data['monthly_usage'][month]['cost'] += cost
        
        # Update endpoint totals
        if endpoint not in self.usage_data['endpoint_usage']:
            self.usage_data['endpoint_usage'][endpoint] = {
                'total_count': 0,
                'total_cost': 0,
                'total_tokens': 0,
                'total_input_tokens': 0,
                'total_output_tokens': 0,
                'models_used': {}
            }
        
        self.usage_data['endpoint_usage'][endpoint]['total_count'] += count
        self.usage_data['endpoint_usage'][endpoint]['total_cost'] += cost
        self.usage_data['endpoint_usage'][endpoint]['total_tokens'] += total_tokens
        self.usage_data['endpoint_usage'][endpoint]['total_input_tokens'] += input_tokens
        self.usage_data['endpoint_usage'][endpoint]['total_output_tokens'] += output_tokens
        
        # Track model usage
        if model not in self.usage_data['endpoint_usage'][endpoint]['models_used']:
            self.usage_data['endpoint_usage'][endpoint]['models_used'][model] = {
                'count': 0,
                'cost': 0
            }
        self.usage_data['endpoint_usage'][endpoint]['models_used'][model]['count'] += count
        self.usage_data['endpoint_usage'][endpoint]['models_used'][model]['cost'] += cost
        
        # Save data
        self.save_usage_data()
        
        return cost
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        today = datetime.now().strftime('%Y-%m-%d')
        current_month = datetime.now().strftime('%Y-%m')
        
        # Calculate 7-day history
        last_7_days = []
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            if date in self.usage_data['daily_usage']:
                last_7_days.append({
                    'date': date,
                    'requests': self.usage_data['daily_usage'][date]['requests'],
                    'cost': self.usage_data['daily_usage'][date]['cost']
                })
            else:
                last_7_days.append({
                    'date': date,
                    'requests': 0,
                    'cost': 0
                })
        
        # Get today's usage
        today_data = self.usage_data['daily_usage'].get(today, {
            'requests': 0,
            'cost': 0,
            'endpoints': {}
        })
        
        # Get current month data
        month_data = self.usage_data['monthly_usage'].get(current_month, {
            'requests': 0,
            'cost': 0
        })
        
        # Calculate endpoint breakdown with descriptions
        endpoint_breakdown = []
        for endpoint, data in self.usage_data['endpoint_usage'].items():
            endpoint_info = self.endpoints.get(endpoint, {})
            endpoint_breakdown.append({
                'endpoint': endpoint,
                'description': endpoint_info.get('description', endpoint),
                'count': data['total_count'],
                'cost': data['total_cost'],
                'avg_cost': data['total_cost'] / data['total_count'] if data['total_count'] > 0 else 0,
                'total_tokens': data.get('total_tokens', 0),
                'input_tokens': data.get('total_input_tokens', 0),
                'output_tokens': data.get('total_output_tokens', 0),
                'models_used': data.get('models_used', {})
            })
        
        # Sort by cost
        endpoint_breakdown.sort(key=lambda x: x['cost'], reverse=True)
        
        # Calculate cost projections
        days_in_month = 30
        if month_data['requests'] > 0:
            days_passed = datetime.now().day
            daily_avg = month_data['cost'] / days_passed
            projected_monthly = daily_avg * days_in_month
        else:
            projected_monthly = 0
        
        return {
            'summary': {
                'total_requests': self.usage_data['total_requests'],
                'total_cost': round(self.usage_data['total_cost'], 4),
                'today_requests': today_data['requests'],
                'today_cost': round(today_data['cost'], 4),
                'month_requests': month_data['requests'],
                'month_cost': round(month_data['cost'], 4),
                'projected_monthly_cost': round(projected_monthly, 2)
            },
            'last_7_days': last_7_days,
            'endpoint_breakdown': endpoint_breakdown,
            'today_breakdown': today_data.get('endpoints', {}),
            'models': self.models,
            'endpoints_config': self.endpoints,
            'current_model': self.current_model
        }
    
    def reset_usage(self, period: str = 'all'):
        """Reset usage data for a specific period"""
        if period == 'all':
            self.usage_data = {
                'total_requests': 0,
                'total_cost': 0,
                'daily_usage': {},
                'endpoint_usage': {},
                'monthly_usage': {}
            }
        elif period == 'today':
            today = datetime.now().strftime('%Y-%m-%d')
            if today in self.usage_data['daily_usage']:
                del self.usage_data['daily_usage'][today]
        elif period == 'month':
            month = datetime.now().strftime('%Y-%m')
            if month in self.usage_data['monthly_usage']:
                del self.usage_data['monthly_usage'][month]
        
        self.save_usage_data()
    
    def set_model(self, model: str):
        """Change the current model being used"""
        if model in self.models:
            self.current_model = model
            return True
        return False
    
    def get_model_cost_estimate(self, endpoint: str, model: str = None) -> Dict[str, float]:
        """Get cost estimate for an endpoint with a specific model"""
        if model is None:
            model = self.current_model
            
        if model not in self.models or endpoint not in self.endpoints:
            return {'error': 'Invalid model or endpoint'}
            
        model_pricing = self.models[model]
        endpoint_config = self.endpoints[endpoint]
        
        # Get costs
        complexity = endpoint_config.get('request_complexity', 'low')
        request_cost_key = f'request_cost_{complexity}'
        request_cost = model_pricing.get(request_cost_key, 0.005)
        
        input_tokens = endpoint_config.get('input_tokens_avg', 100)
        output_tokens = endpoint_config.get('output_tokens_avg', 100)
        
        input_cost = (input_tokens / 1_000_000) * model_pricing['input_cost_per_1m']
        output_cost = (output_tokens / 1_000_000) * model_pricing['output_cost_per_1m']
        
        return {
            'model': model_pricing['name'],
            'request_cost': request_cost,
            'input_cost': input_cost,
            'output_cost': output_cost,
            'total_cost': request_cost + input_cost + output_cost,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens
        }

# Global instance
usage_tracker = UsageTracker()
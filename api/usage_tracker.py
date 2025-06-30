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
        # Using llama-3.1-sonar-small-128k-online model pricing:
        # $5 per 1,000 requests + $0.2 per 1M tokens ($0.0002 per 1K tokens)
        self.pricing = {
            'analyze_business': {
                'tokens_avg': 500,  # ~250 input + 250 output
                'cost_per_request': 0.005,  # $5/1000 requests = $0.005 per request
                'cost_per_1k_tokens': 0.0002,  # $0.2/1M tokens = $0.0002 per 1K tokens
                'description': 'Business analysis with AI'
            },
            'generate_keywords': {
                'tokens_avg': 300,  # ~150 input + 150 output
                'cost_per_request': 0.005,
                'cost_per_1k_tokens': 0.0002,
                'description': 'Keyword generation'
            },
            'generate_keywords_seed': {
                'tokens_avg': 100,  # Minimal tokens for suggestions
                'cost_per_request': 0.005,
                'cost_per_1k_tokens': 0.0002,
                'description': 'Seed keyword suggestions'
            },
            'generate_content': {
                'tokens_avg': 2500,  # ~500 input + 2000 output
                'cost_per_request': 0.005,
                'cost_per_1k_tokens': 0.0002,
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
    
    def track_usage(self, endpoint: str, tokens: int = None, count: int = 1):
        """Track API usage for an endpoint"""
        today = datetime.now().strftime('%Y-%m-%d')
        month = datetime.now().strftime('%Y-%m')
        
        # Use estimated tokens if not provided
        if tokens is None and endpoint in self.pricing:
            tokens = self.pricing[endpoint]['tokens_avg'] * count
        
        # Calculate cost (per-request fee + token cost)
        cost = 0
        if endpoint in self.pricing:
            # Add per-request fee
            cost = self.pricing[endpoint]['cost_per_request'] * count
            # Add token cost if tokens provided
            if tokens:
                cost += (tokens / 1000) * self.pricing[endpoint]['cost_per_1k_tokens']
        
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
                'tokens': 0
            }
        
        self.usage_data['daily_usage'][today]['endpoints'][endpoint]['count'] += count
        self.usage_data['daily_usage'][today]['endpoints'][endpoint]['cost'] += cost
        self.usage_data['daily_usage'][today]['endpoints'][endpoint]['tokens'] += tokens or 0
        
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
                'total_tokens': 0
            }
        
        self.usage_data['endpoint_usage'][endpoint]['total_count'] += count
        self.usage_data['endpoint_usage'][endpoint]['total_cost'] += cost
        self.usage_data['endpoint_usage'][endpoint]['total_tokens'] += tokens or 0
        
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
            pricing_info = self.pricing.get(endpoint, {})
            endpoint_breakdown.append({
                'endpoint': endpoint,
                'description': pricing_info.get('description', endpoint),
                'count': data['total_count'],
                'cost': data['total_cost'],
                'avg_cost': data['total_cost'] / data['total_count'] if data['total_count'] > 0 else 0,
                'tokens': data['total_tokens']
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
            'pricing_info': self.pricing
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

# Global instance
usage_tracker = UsageTracker()
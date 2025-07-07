import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { id } = req.query;
  
  if (req.method === 'GET') {
    // Return mock project details
    const mockProject = {
      id: id,
      name: 'Sample Project',
      business_input: 'Digital marketing agency specializing in SEO and PPC',
      business_analysis: {
        business_name: 'Sample Marketing Agency',
        business_description: 'A digital marketing agency helping businesses grow online',
        target_audience: 'Small to medium businesses',
        core_offerings: ['SEO Services', 'PPC Management', 'Content Marketing', 'Social Media Marketing'],
        template_opportunities: [
          {
            template_name: 'Location-based Services',
            template_pattern: '[Service] in [City]',
            example_pages: [
              'SEO Services in New York',
              'PPC Management in Los Angeles',
              'Content Marketing in Chicago'
            ],
            estimated_pages: 500,
            difficulty: 'Low'
          },
          {
            template_name: 'Service Comparisons',
            template_pattern: '[Service A] vs [Service B]',
            example_pages: [
              'SEO vs PPC',
              'Google Ads vs Facebook Ads', 
              'Email Marketing vs Social Media'
            ],
            estimated_pages: 150,
            difficulty: 'Medium'
          }
        ]
      },
      created_at: new Date().toISOString()
    };
    
    res.status(200).json(mockProject);
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}
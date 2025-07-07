import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    // Return mock projects for now
    const mockProjects = [
      {
        id: '1',
        name: 'Sample Project',
        business_input: 'Digital marketing agency',
        business_analysis: {
          business_name: 'Sample Marketing Agency',
          business_description: 'A sample digital marketing agency',
          template_opportunities: [
            {
              template_name: 'Location-based Services',
              template_pattern: '[Service] in [City]',
              example_pages: ['SEO in New York', 'PPC in Los Angeles'],
              estimated_pages: 500,
              difficulty: 'Low'
            }
          ]
        },
        created_at: new Date().toISOString()
      }
    ];
    
    res.status(200).json(mockProjects);
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}
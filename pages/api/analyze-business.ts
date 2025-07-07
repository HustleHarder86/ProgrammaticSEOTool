import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const { business_input } = req.body;
    
    // Return mock analysis result
    const mockResponse = {
      project_id: Date.now().toString(),
      business_name: 'Sample Business',
      business_description: business_input || 'A sample business description',
      target_audience: 'Small to medium businesses',
      core_offerings: ['Service 1', 'Service 2', 'Service 3'],
      template_opportunities: [
        {
          template_name: 'Location-based Pages',
          template_pattern: '[Service] in [City]',
          example_pages: [
            'Digital Marketing in New York',
            'SEO Services in Los Angeles', 
            'PPC Management in Chicago'
          ],
          estimated_pages: 250,
          difficulty: 'Low'
        },
        {
          template_name: 'Service Comparisons', 
          template_pattern: '[Service A] vs [Service B]',
          example_pages: [
            'SEO vs PPC',
            'Google Ads vs Facebook Ads',
            'Email Marketing vs Social Media Marketing'
          ],
          estimated_pages: 150,
          difficulty: 'Medium'
        }
      ]
    };
    
    res.status(200).json(mockResponse);
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}
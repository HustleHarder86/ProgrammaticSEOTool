import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    // Return mock templates
    res.status(200).json([]);
  } else if (req.method === 'POST') {
    // Mock template creation
    res.status(200).json({ 
      id: Date.now().toString(),
      message: 'Template created successfully (mock)' 
    });
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}
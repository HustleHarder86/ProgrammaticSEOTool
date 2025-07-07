import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    // Return mock exports
    res.status(200).json({ exports: [] });
  } else if (req.method === 'POST') {
    // Mock export creation
    res.status(200).json({ 
      export_id: Date.now().toString(),
      status: 'pending',
      message: 'Export started (mock)' 
    });
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}
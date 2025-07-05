import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // For now, return a message that the API is being set up
  res.status(200).json({ 
    message: 'API endpoint working. Python integration coming soon.',
    path: req.query.path,
    method: req.method 
  });
}
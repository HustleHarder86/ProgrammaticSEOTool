import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* Proxy API requests to FastAPI backend */
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: '/api/:path*', // This will be handled by Vercel's api/ directory
      },
    ];
  },
};

export default nextConfig;
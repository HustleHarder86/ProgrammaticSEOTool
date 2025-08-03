import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from './providers';
import { Sidebar } from '@/components/layout/Sidebar';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'SEO Toolkit',
  description: 'Personal programmatic SEO toolkit for bulk page generation',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          <div className="flex h-screen bg-gray-50">
            <Sidebar />
            <main className="flex-1 lg:ml-64 transition-all duration-300 overflow-y-auto">
              <div className="p-4 sm:p-6 lg:p-8 min-h-full">
                {children}
              </div>
            </main>
          </div>
        </Providers>
      </body>
    </html>
  );
}
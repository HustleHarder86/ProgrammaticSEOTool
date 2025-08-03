'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { 
  Home, 
  FolderOpen, 
  LayoutTemplate, 
  Database, 
  Download,
  Settings,
  Menu,
  X,
  ChevronRight,
  Sparkles,
  BarChart3,
  FileText,
  Zap
} from 'lucide-react';

export function Sidebar() {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  const navItems = [
    { 
      href: '/', 
      label: 'Dashboard', 
      icon: Home,
      description: 'Overview and analytics'
    },
    { 
      href: '/projects', 
      label: 'Projects', 
      icon: FolderOpen,
      description: 'Manage your SEO projects'
    },
    { 
      href: '/analyze', 
      label: 'AI Analysis', 
      icon: Sparkles,
      description: 'Analyze businesses with AI'
    },
    { 
      href: '/templates', 
      label: 'Templates', 
      icon: LayoutTemplate,
      description: 'Page templates library'
    },
    { 
      href: '/data', 
      label: 'Data', 
      icon: Database,
      description: 'Import and manage data'
    },
    { 
      href: '/export', 
      label: 'Export', 
      icon: Download,
      description: 'Export generated pages'
    },
    { 
      href: '/costs', 
      label: 'Cost Tracking', 
      icon: BarChart3,
      description: 'Monitor API costs'
    },
    { 
      href: '/settings', 
      label: 'Settings', 
      icon: Settings,
      description: 'Configure your toolkit'
    },
  ];

  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={() => setIsMobileOpen(!isMobileOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-md bg-white shadow-md border border-gray-200"
      >
        {isMobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
      </button>

      {/* Mobile overlay */}
      {isMobileOpen && (
        <div 
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => setIsMobileOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed top-0 left-0 h-full bg-white border-r border-gray-200 z-40
        transition-all duration-300 ease-in-out
        ${isCollapsed ? 'w-16' : 'w-64'}
        ${isMobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        {/* Header */}
        <div className="h-16 flex items-center justify-between px-4 border-b border-gray-200">
          {!isCollapsed && (
            <Link href="/" className="flex items-center space-x-2">
              <Zap className="w-8 h-8 text-purple-600" />
              <span className="text-xl font-bold text-gray-900">SEO Toolkit</span>
            </Link>
          )}
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="hidden lg:flex p-1.5 rounded-md hover:bg-gray-100 transition-colors"
          >
            <ChevronRight className={`w-5 h-5 text-gray-600 transition-transform ${isCollapsed ? '' : 'rotate-180'}`} />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto py-4">
          <ul className="space-y-1 px-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href || 
                             (item.href !== '/' && pathname.startsWith(item.href));
              
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    onClick={() => setIsMobileOpen(false)}
                    className={`
                      group flex items-center px-3 py-2.5 rounded-lg transition-all
                      ${isActive 
                        ? 'bg-purple-50 text-purple-700 font-medium' 
                        : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                      }
                    `}
                  >
                    <Icon className={`
                      flex-shrink-0 transition-colors
                      ${isCollapsed ? 'w-6 h-6' : 'w-5 h-5 mr-3'}
                      ${isActive ? 'text-purple-600' : 'text-gray-400 group-hover:text-gray-600'}
                    `} />
                    
                    {!isCollapsed && (
                      <div className="flex-1">
                        <div className="text-sm">{item.label}</div>
                        {item.description && (
                          <div className="text-xs text-gray-500 mt-0.5">{item.description}</div>
                        )}
                      </div>
                    )}

                    {/* Tooltip for collapsed state */}
                    {isCollapsed && (
                      <div className="
                        absolute left-full ml-2 px-2 py-1 bg-gray-900 text-white text-sm rounded
                        opacity-0 pointer-events-none group-hover:opacity-100 transition-opacity
                        whitespace-nowrap z-50
                      ">
                        {item.label}
                      </div>
                    )}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200">
          {!isCollapsed ? (
            <div className="text-xs text-gray-500">
              <div className="font-medium mb-1">Programmatic SEO</div>
              <div>Generate pages at scale</div>
            </div>
          ) : (
            <div className="flex justify-center">
              <Sparkles className="w-5 h-5 text-gray-400" />
            </div>
          )}
        </div>
      </aside>
    </>
  );
}
/**
 * Layout Component - Main application shell
 * FOSSEE Scientific Analytics UI
 */
import { NavLink, Outlet } from 'react-router-dom';

export default function Layout() {
  return (
    <div className="min-h-screen bg-bg-main flex flex-col">
      {/* Header */}
      <header className="bg-primary-900 text-white shadow-card">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo & Title */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-primary-700 rounded-lg flex items-center justify-center">
                <svg 
                  className="w-6 h-6" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" 
                  />
                </svg>
              </div>
              <div>
                <h1 className="font-serif text-xl font-semibold">
                  Chemical Equipment Visualizer
                </h1>
                <p className="text-sm text-primary-700 opacity-80">
                  FOSSEE Scientific Analytics
                </p>
              </div>
            </div>

            {/* Navigation */}
            <nav className="flex items-center gap-2">
              <NavLink 
                to="/" 
                className={({ isActive }) => 
                  `nav-link ${isActive ? 'bg-primary-700 text-white' : ''}`
                }
                end
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                Upload
              </NavLink>
              <NavLink 
                to="/dashboard" 
                className={({ isActive }) => 
                  `nav-link ${isActive ? 'bg-primary-700 text-white' : ''}`
                }
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                Dashboard
              </NavLink>
              <NavLink 
                to="/history" 
                className={({ isActive }) => 
                  `nav-link ${isActive ? 'bg-primary-700 text-white' : ''}`
                }
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                History
              </NavLink>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-border py-6">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-text-secondary text-sm">
            Chemical Equipment Parameter Visualizer • 
            <a 
              href="https://fossee.in" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-primary-700 hover:text-primary-600 ml-1"
            >
              FOSSEE Project
            </a>
            {' '}• IIT Bombay
          </p>
        </div>
      </footer>
    </div>
  );
}

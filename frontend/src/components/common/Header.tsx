import { Link, useLocation } from 'react-router-dom';

const Header = () => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="bg-primary text-white shadow-md">
      <div className="container mx-auto py-4 px-4 flex justify-between items-center">
        <div className="text-2xl font-bold">
          <Link to="/" className="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
            </svg>
            HarborLink
          </Link>
        </div>
        <nav>
          <ul className="flex space-x-6">
            <li>
              <Link 
                to="/" 
                className={`hover:text-white/80 ${isActive('/') ? 'border-b-2 border-white font-medium' : ''}`}
              >
                Home
              </Link>
            </li>
            <li>
              <Link 
                to="/generate" 
                className={`hover:text-white/80 ${isActive('/generate') ? 'border-b-2 border-white font-medium' : ''}`}
              >
                Generate
              </Link>
            </li>
            <li>
              <Link 
                to="/projects" 
                className={`hover:text-white/80 ${isActive('/projects') ? 'border-b-2 border-white font-medium' : ''}`}
              >
                Projects
              </Link>
            </li>
            <li>
              <a 
                href="/docs" 
                target="_blank" 
                rel="noopener noreferrer"
                className="ml-4 bg-white text-primary px-3 py-1 rounded-md hover:bg-gray-100 transition-colors"
              >
                API Docs
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
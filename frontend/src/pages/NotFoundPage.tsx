import { Link } from 'react-router-dom';

const NotFoundPage = () => {
  return (
    <div className="container mx-auto px-4 py-12 text-center">
      <div className="max-w-md mx-auto">
        <h1 className="text-9xl font-bold text-primary">404</h1>
        <h2 className="text-2xl font-bold mt-4 mb-2">Page Not Found</h2>
        <p className="text-gray-600 mb-8">The page you are looking for does not exist or has been moved.</p>
        <Link 
          to="/" 
          className="bg-primary text-white px-6 py-3 rounded-md hover:bg-primary-dark inline-flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7m-7-7v14" />
          </svg>
          Return Home
        </Link>
      </div>
    </div>
  );
};

export default NotFoundPage;
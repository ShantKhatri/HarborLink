import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getProject } from '../services/projectsService';

interface Project {
  id: string;
  api_name: string;
  framework: string;
  target_standard: string;
  created_at: string;
  updated_at: string;
  generated_code?: Record<string, string>;
}

const ProjectDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<string>('');

  useEffect(() => {
    const fetchProject = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        const data = await getProject(id);
        setProject(data);
        
        // Set the first code file as active tab
        if (data.generated_code && Object.keys(data.generated_code).length > 0) {
          setActiveTab(Object.keys(data.generated_code)[0]);
        }
      } catch (err) {
        setError('Failed to load project details. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProject();
  }, [id]);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 flex justify-center items-center h-64">
        <svg className="animate-spin h-10 w-10 text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="container mx-auto px-4">
        <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-md mb-4">
          {error || 'Project not found'}
        </div>
        <Link to="/projects" className="bg-primary text-white px-4 py-2 rounded-md hover:bg-primary-dark">
          Back to Projects
        </Link>
      </div>
    );
  }

  const getFrameworkColor = (framework: string) => {
    return framework === 'fastapi' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800';
  };

  return (
    <div className="container mx-auto px-4">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">{project.api_name}</h1>
          <p className="text-gray-500">Project ID: {project.id}</p>
        </div>
        <div className="flex space-x-3 mt-4 md:mt-0">
          <a 
            href={`/api/middleware/download/${project.id}`}
            className="flex items-center bg-primary text-white px-4 py-2 rounded-md hover:bg-primary-dark"
            target="_blank"
            rel="noopener noreferrer"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Download
          </a>
          <Link 
            to="/projects" 
            className="flex items-center border border-gray-300 bg-white px-4 py-2 rounded-md hover:bg-gray-50"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Projects
          </Link>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-bold mb-4">Project Details</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <span className="text-gray-500 text-sm">Framework</span>
            <div className="mt-1">
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getFrameworkColor(project.framework)}`}>
                {project.framework === 'fastapi' ? 'FastAPI (Python)' : 'Express.js (Node.js)'}
              </span>
            </div>
          </div>
          <div>
            <span className="text-gray-500 text-sm">Target Standard</span>
            <div className="mt-1">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {project.target_standard.toUpperCase()}
              </span>
            </div>
          </div>
          <div>
            <span className="text-gray-500 text-sm">Created</span>
            <div className="mt-1 font-medium">{formatDate(project.created_at)}</div>
          </div>
          <div>
            <span className="text-gray-500 text-sm">Last Updated</span>
            <div className="mt-1 font-medium">{formatDate(project.updated_at)}</div>
          </div>
        </div>
      </div>

      {project.generated_code && Object.keys(project.generated_code).length > 0 && (
        <div className="bg-white rounded-lg shadow-md overflow-hidden mb-8">
          <div className="border-b border-gray-200 px-6 py-4">
            <h2 className="text-xl font-bold">Generated Code</h2>
          </div>
          <div className="border-b border-gray-200 bg-gray-50 px-2">
            <nav className="flex overflow-x-auto">
              {Object.keys(project.generated_code).map((filename) => (
                <button 
                  key={filename}
                  className={`py-3 px-4 text-sm font-medium border-b-2 whitespace-nowrap ${activeTab === filename ? 'border-primary text-primary' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
                  onClick={() => setActiveTab(filename)}
                >
                  {filename}
                </button>
              ))}
            </nav>
          </div>
          <div className="p-6 bg-gray-900 text-white overflow-auto" style={{ maxHeight: '400px' }}>
            <pre className="text-sm font-mono whitespace-pre">{project.generated_code[activeTab]}</pre>
          </div>
        </div>
      )}

      <div className="bg-white rounded-lg shadow-md overflow-hidden mb-8">
        <div className="border-b border-gray-200 px-6 py-4">
          <h2 className="text-xl font-bold">Deployment Instructions</h2>
        </div>
        <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="border rounded-lg p-4">
            <h3 className="text-lg font-semibold mb-4">Option 1: Manual Installation</h3>
            <ol className="list-decimal list-inside space-y-3 text-gray-700">
              <li>Download the middleware package</li>
              <li>Extract the ZIP file to your server</li>
              <li>
                Install dependencies:
                <div className="mt-1 bg-gray-100 p-2 rounded font-mono text-sm">
                  {project.framework === 'fastapi' 
                    ? 'pip install -r requirements.txt' 
                    : 'npm install'}
                </div>
              </li>
              <li>
                Run the middleware:
                <div className="mt-1 bg-gray-100 p-2 rounded font-mono text-sm">
                  {project.framework === 'fastapi' 
                    ? 'uvicorn main:app --host 0.0.0.0 --port 8000' 
                    : 'node app.js'}
                </div>
              </li>
            </ol>
          </div>
          <div className="border rounded-lg p-4">
            <h3 className="text-lg font-semibold mb-4">Option 2: Docker Deployment</h3>
            <ol className="list-decimal list-inside space-y-3 text-gray-700">
              <li>Download the middleware package</li>
              <li>Extract the ZIP file</li>
              <li>
                Build the Docker image:
                <div className="mt-1 bg-gray-100 p-2 rounded font-mono text-sm">
                  docker build -t harborlink-middleware .
                </div>
              </li>
              <li>
                Run the container:
                <div className="mt-1 bg-gray-100 p-2 rounded font-mono text-sm">
                  docker run -p 8000:8000 harborlink-middleware
                </div>
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectDetailPage;
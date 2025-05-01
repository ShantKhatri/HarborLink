import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyzeApiSpec, generateMiddleware } from '../services/middlewareService';

const GeneratePage = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [file, setFile] = useState<File | null>(null);
  const [apiSpec, setApiSpec] = useState<any | null>(null);
  const [framework, setFramework] = useState('fastapi');
  const [targetStandard, setTargetStandard] = useState('ondc');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generationResult, setGenerationResult] = useState<any | null>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    setLoading(true);
    setError(null);
    setFile(selectedFile);

    try {
      const result = await analyzeApiSpec(selectedFile);
      setApiSpec(result);
      setStep(2);
    } catch (err) {
      setError('Failed to analyze API specification. Please check the file format.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const result = await generateMiddleware(file, framework, targetStandard);
      setGenerationResult(result);
      setStep(3);
    } catch (err) {
      setError('Failed to generate middleware. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = () => {
    switch (step) {
      case 1:
        return (
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-2xl font-bold mb-6">Upload API Specification</h2>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-10 text-center hover:border-primary transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" className="mx-auto h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <p className="my-4 text-gray-600">Upload your bank's OpenAPI 3.0 specification in JSON or YAML format</p>
              <input
                type="file"
                id="file-input"
                className="hidden"
                accept=".json,.yaml,.yml"
                onChange={handleFileUpload}
              />
              <label 
                htmlFor="file-input" 
                className="bg-primary text-white px-6 py-3 rounded-md cursor-pointer hover:bg-primary-dark transition-colors inline-block"
              >
                Choose File
              </label>
              {file && (
                <p className="mt-4 text-sm text-gray-600 bg-gray-100 p-2 rounded">
                  Selected: {file.name}
                </p>
              )}
            </div>
            {error && (
              <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}
            {loading && (
              <div className="mt-4 flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing API...
              </div>
            )}
          </div>
        );
      case 2:
        return (
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-2xl font-bold mb-6">Configure Middleware</h2>
            {apiSpec && (
              <div className="mb-6 bg-gray-50 p-4 rounded-lg border border-gray-200">
                <h3 className="text-lg font-medium mb-2">API Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <span className="text-gray-600 text-sm">API Name:</span>
                    <p className="font-medium">{apiSpec.api_name}</p>
                  </div>
                  <div>
                    <span className="text-gray-600 text-sm">Version:</span>
                    <p className="font-medium">{apiSpec.version}</p>
                  </div>
                  <div>
                    <span className="text-gray-600 text-sm">Endpoints:</span>
                    <p className="font-medium">{apiSpec.endpoint_count}</p>
                  </div>
                </div>
              </div>
            )}
            <div className="space-y-6">
              <div className="form-group">
                <label htmlFor="framework" className="block text-sm font-medium text-gray-700 mb-1">
                  Framework:
                </label>
                <select
                  id="framework"
                  className="block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                  value={framework}
                  onChange={(e) => setFramework(e.target.value)}
                >
                  <option value="fastapi">FastAPI (Python)</option>
                  <option value="express">Express.js (Node.js)</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="target-standard" className="block text-sm font-medium text-gray-700 mb-1">
                  Target Standard:
                </label>
                <select
                  id="target-standard"
                  className="block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
                  value={targetStandard}
                  onChange={(e) => setTargetStandard(e.target.value)}
                >
                  <option value="ondc">ONDC</option>
                  <option value="ocen">OCEN</option>
                </select>
              </div>
            </div>
            <div className="mt-8 flex justify-between">
              <button 
                className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50" 
                onClick={() => setStep(1)}
              >
                Back
              </button>
              <button 
                className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed" 
                onClick={handleGenerate} 
                disabled={loading}
              >
                {loading ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Generating...
                  </span>
                ) : 'Generate Middleware'}
              </button>
            </div>
            {error && (
              <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}
          </div>
        );
      case 3:
        return (
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-2xl font-bold mb-6">Middleware Generated</h2>
            {generationResult && (
              <div>
                <div className="mb-6 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
                  <div className="flex">
                    <svg className="h-6 w-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                    </svg>
                    <span className="font-medium">Middleware generated successfully!</span>
                  </div>
                </div>
                <div className="bg-gray-50 rounded-lg p-4 mb-6 border border-gray-200">
                  <h3 className="font-medium text-lg mb-2">Generation Summary</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <span className="text-gray-600 text-sm">API Name:</span>
                      <p className="font-medium">{generationResult.api_name}</p>
                    </div>
                    <div>
                      <span className="text-gray-600 text-sm">Framework:</span>
                      <p className="font-medium">{framework === 'fastapi' ? 'FastAPI (Python)' : 'Express.js (Node.js)'}</p>
                    </div>
                    <div>
                      <span className="text-gray-600 text-sm">Target Standard:</span>
                      <p className="font-medium">{targetStandard.toUpperCase()}</p>
                    </div>
                    <div>
                      <span className="text-gray-600 text-sm">Endpoints Processed:</span>
                      <p className="font-medium">{generationResult.endpoint_count || 0}</p>
                    </div>
                  </div>
                </div>
                <div className="flex flex-wrap gap-4 mt-6">
                  <a
                    href={`/api/middleware/download/${generationResult.project_id}`}
                    className="flex items-center bg-primary text-white px-4 py-2 rounded-md hover:bg-primary-dark"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    Download Middleware
                  </a>
                  <button
                    className="flex items-center border border-primary text-primary px-4 py-2 rounded-md hover:bg-blue-50"
                    onClick={() => navigate(`/projects/${generationResult.project_id}`)}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    View Project Details
                  </button>
                </div>
              </div>
            )}
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="container mx-auto px-4">
      <h1 className="text-3xl font-bold mb-8">Generate Middleware</h1>
      
      {/* Step Progress Indicator */}
      <div className="mb-10">
        <div className="flex items-center">
          <div className={`flex items-center justify-center w-10 h-10 rounded-full ${step >= 1 ? 'bg-primary text-white' : 'bg-gray-200'}`}>
            1
          </div>
          <div className={`flex-1 h-1 mx-2 ${step >= 2 ? 'bg-primary' : 'bg-gray-200'}`}></div>
          <div className={`flex items-center justify-center w-10 h-10 rounded-full ${step >= 2 ? 'bg-primary text-white' : 'bg-gray-200'}`}>
            2
          </div>
          <div className={`flex-1 h-1 mx-2 ${step >= 3 ? 'bg-primary' : 'bg-gray-200'}`}></div>
          <div className={`flex items-center justify-center w-10 h-10 rounded-full ${step >= 3 ? 'bg-primary text-white' : 'bg-gray-200'}`}>
            3
          </div>
        </div>
        <div className="flex justify-between mt-2">
          <div className={`text-sm ${step >= 1 ? 'text-primary font-medium' : 'text-gray-500'}`}>Upload</div>
          <div className={`text-sm ${step >= 2 ? 'text-primary font-medium' : 'text-gray-500'}`}>Configure</div>
          <div className={`text-sm ${step >= 3 ? 'text-primary font-medium' : 'text-gray-500'}`}>Generate</div>
        </div>
      </div>
      
      {renderStepContent()}
    </div>
  );
};

export default GeneratePage;
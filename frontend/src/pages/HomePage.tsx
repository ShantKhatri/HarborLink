import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="container mx-auto">
      {/* Hero Section */}
      <section className="text-center py-16 px-4 mb-16">
        <h1 className="text-5xl font-bold mb-6 text-primary">HarborLink</h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-10">
          AI-powered middleware generator that converts bank APIs into ONDC/OCEN compliant interfaces.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Link 
            to="/generate" 
            className="bg-primary text-white px-6 py-3 rounded-lg hover:bg-primary-dark transition-colors"
          >
            Start Generating
          </Link>
          <a 
            href="/docs" 
            className="border border-primary text-primary px-6 py-3 rounded-lg hover:bg-blue-50 transition-colors"
            target="_blank" 
            rel="noopener noreferrer"
          >
            API Documentation
          </a>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-12">
        <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
            <div className="text-primary text-4xl mb-4 flex justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-center mb-3">Upload API Specifications</h3>
            <p className="text-gray-600 text-center">
              Seamlessly upload your bank's OpenAPI 3.0 specification files to begin the transformation process.
            </p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
            <div className="text-secondary text-4xl mb-4 flex justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-center mb-3">AI-Powered Transformation</h3>
            <p className="text-gray-600 text-center">
              Our GenAI engine automatically maps your APIs to ONDC/OCEN standards, generating compliant middleware.
            </p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow">
            <div className="text-primary text-4xl mb-4 flex justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-center mb-3">Deploy with Ease</h3>
            <p className="text-gray-600 text-center">
              Download the generated middleware or deploy directly to your infrastructure with our containerized solution.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-primary to-primary-dark text-white rounded-xl my-16 py-12 px-6">
        <div className="text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to transform your APIs?</h2>
          <p className="text-xl mb-8">Get started with HarborLink today and streamline your ONDC/OCEN compliance.</p>
          <Link 
            to="/generate" 
            className="bg-white text-primary px-6 py-3 rounded-lg hover:bg-gray-100 transition-colors"
          >
            Generate Middleware
          </Link>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
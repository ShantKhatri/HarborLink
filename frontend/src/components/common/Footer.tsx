const Footer = () => {
  return (
    <footer className="bg-gray-100 py-8 border-t border-gray-200 mt-auto">
      <div className="container mx-auto text-center">
        <p className="text-gray-600 mb-2">
          HarborLink - AI-Powered Middleware for ONDC/OCEN API Compliance
        </p>
        <p className="text-gray-500 text-sm">
          &copy; {new Date().getFullYear()} Prashantkumar Khatri
        </p>
      </div>
    </footer>
  );
};

export default Footer;
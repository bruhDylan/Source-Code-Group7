
import React from 'react';

const EmptyState: React.FC = () => {
  return (
    <div className="flex-1 flex items-center justify-center min-h-screen">
      <div className="text-center max-w-2xl mx-auto px-6">
        <h1 
          className="text-6xl md:text-7xl font-bold text-gray-800 mb-4 leading-tight"
          style={{ fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", Arial, sans-serif' }}
        >
          How can we <span className="text-cyan-500">assist</span> you today?
        </h1>
      </div>
    </div>
  );
};

export default EmptyState;

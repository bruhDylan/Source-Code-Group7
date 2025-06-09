
import React from 'react';
import { Menu } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface AppHeaderProps {
  onToggleSidebar: () => void;
}

const AppHeader: React.FC<AppHeaderProps> = ({ onToggleSidebar }) => {
  return (
    <div className="fixed top-0 left-0 right-0 z-30 flex justify-between items-center p-4">
      <div className="lg:hidden">
        <Button
          variant="ghost"
          size="sm"
          onClick={onToggleSidebar}
          className="text-gray-700 hover:text-gray-900 hover:bg-white/80 backdrop-blur-sm border border-gray-200 shadow-sm"
        >
          <Menu className="w-5 h-5" />
        </Button>
      </div>
    </div>
  );
};

export default AppHeader;

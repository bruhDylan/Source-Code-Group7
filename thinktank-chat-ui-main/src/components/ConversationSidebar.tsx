
import React from 'react';
import { Button } from '@/components/ui/button';
import { Plus, LogOut } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from 'sonner';

interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

interface ConversationSidebarProps {
  conversations: Conversation[];
  currentConversationId: string | null;
  onSelectConversation: (id: string) => void;
  onNewConversation: () => void;
  onDeleteConversation: (id: string) => void;
  isOpen: boolean;
  onClose: () => void;
}

const ConversationSidebar: React.FC<ConversationSidebarProps> = ({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
  onDeleteConversation,
  isOpen,
  onClose,
}) => {
  const { user, signOut } = useAuth();

  const handleSignOut = async () => {
    try {
      await signOut();
      toast.success('Signed out successfully');
    } catch (error) {
      toast.error('Error signing out');
    }
  };

  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden" 
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <div className={`
        fixed top-0 left-0 h-screen w-80 bg-gray-900 z-50 transform transition-transform duration-300 ease-in-out flex flex-col
        lg:relative lg:translate-x-0 lg:z-auto
        ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        {/* Header */}
        <div className="p-6 border-b border-gray-700">
          {/* Logo */}
          <div className="flex justify-center mb-6">
            <img 
              src="/lovable-uploads/7facae2b-c7f4-4992-8687-57a0ff34216f.png" 
              alt="Think Tank Logo" 
              className="w-30 h-30 object-contain"
            />
          </div>
          
          <Button
            onClick={onNewConversation}
            className="w-full bg-cyan-500 hover:bg-cyan-600 text-white flex items-center gap-2 rounded-lg py-3"
          >
            <Plus className="w-5 h-5" />
            Begin a New Chat
          </Button>
        </div>
        
        {/* Recent Chats */}
        <div className="flex-1 overflow-y-auto custom-scrollbar">
          <div className="p-6">
            <h3 className="text-gray-400 text-sm font-medium mb-4 uppercase tracking-wider">Recent Chats</h3>
            <div className="space-y-2">
              {conversations.length === 0 ? (
                <div className="text-center py-12 text-gray-500">
                  <p className="text-sm">No conversations yet</p>
                  <p className="text-xs text-gray-600 mt-1">Start a new chat to begin</p>
                </div>
              ) : (
                conversations.map((conversation) => (
                  <div
                    key={conversation.id}
                    className={`p-4 rounded-lg cursor-pointer transition-all duration-200 group relative ${
                      currentConversationId === conversation.id 
                        ? 'bg-gray-800 border-l-4 border-cyan-500' 
                        : 'hover:bg-gray-800'
                    }`}
                    onClick={() => onSelectConversation(conversation.id)}
                  >
                    <div className="flex items-start gap-3">
                      <div className="w-2 h-2 bg-cyan-500 rounded-full mt-2 flex-shrink-0"></div>
                      <div className="flex-1 min-w-0">
                        <h4 className="text-white text-sm font-medium truncate leading-tight">
                          {conversation.title}
                        </h4>
                        <p className="text-gray-400 text-xs mt-2 truncate">
                          {conversation.title.length > 50 ? 'Sure! Here are some strategies...' : 'Click to continue...'}
                        </p>
                        <p className="text-gray-500 text-xs mt-2">
                          {formatDistanceToNow(new Date(conversation.updated_at), { addSuffix: true })}
                        </p>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* User Profile */}
        <div className="p-6 border-t border-gray-700">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-cyan-500 rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-sm">
                {user?.email?.charAt(0).toUpperCase() || 'U'}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-white text-sm font-medium truncate">
                {user?.email || 'User Profile'}
              </p>
              <p className="text-gray-400 text-xs">Professional Services</p>
            </div>
          </div>
          <Button
            onClick={handleSignOut}
            variant="ghost"
            className="w-full text-gray-400 hover:text-white hover:bg-gray-700 flex items-center gap-2 justify-start"
          >
            <LogOut className="w-4 h-4" />
            Sign Out
          </Button>
        </div>
      </div>
    </>
  );
};

export default ConversationSidebar;

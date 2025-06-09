
import React from 'react';
import { Send } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface ChatInputProps {
  prompt: string;
  setPrompt: (prompt: string) => void;
  onSend: () => void;
  loading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ prompt, setPrompt, onSend, loading }) => {
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div className="relative">
      <div className="flex items-center bg-white border border-gray-200 rounded-full shadow-sm">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Type your prompt here"
          disabled={loading}
          className="flex-1 px-6 py-4 bg-transparent border-none outline-none text-gray-600 placeholder-gray-400"
        />
        <Button
          onClick={onSend}
          disabled={loading || !prompt.trim()}
          className="m-2 w-12 h-12 rounded-full bg-cyan-500 hover:bg-cyan-600 text-white flex items-center justify-center p-0"
        >
          <Send className="w-5 h-5" />
        </Button>
      </div>
    </div>
  );
};

export default ChatInput;

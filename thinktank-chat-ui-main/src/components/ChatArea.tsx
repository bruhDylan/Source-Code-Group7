
import React, { useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import LoadingIndicator from './LoadingIndicator';
import EmptyState from './EmptyState';
import ExportButtons from './ExportButtons';
import ChatInput from './ChatInput';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatAreaProps {
  messages: Message[];
  loading: boolean;
  prompt: string;
  setPrompt: (prompt: string) => void;
  onSendPrompt: () => void;
}

const ChatArea: React.FC<ChatAreaProps> = ({ 
  messages, 
  loading, 
  prompt, 
  setPrompt, 
  onSendPrompt 
}) => {
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 flex flex-col min-h-screen bg-gradient-to-br from-white via-blue-50 to-cyan-50">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 && !loading ? (
          <EmptyState />
        ) : (
          <div className="max-w-4xl mx-auto p-6 space-y-6">
            {messages.map((msg, idx) => (
              <ChatMessage key={idx} message={msg} index={idx} />
            ))}
            {loading && <LoadingIndicator />}
            <div ref={chatEndRef} />
          </div>
        )}
      </div>

      {/* Export Buttons - only show when there are messages */}
      {messages.length > 0 && (
        <div className="max-w-4xl mx-auto px-6">
          <ExportButtons messages={messages} />
        </div>
      )}

      {/* Input Area */}
      <div className="max-w-4xl mx-auto w-full px-6 pb-6">
        <ChatInput
          prompt={prompt}
          setPrompt={setPrompt}
          onSend={onSendPrompt}
          loading={loading}
        />
      </div>
    </div>
  );
};

export default ChatArea;

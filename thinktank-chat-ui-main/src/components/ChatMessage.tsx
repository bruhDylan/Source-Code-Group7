
import React from 'react';
import ReactMarkdown from 'react-markdown';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatMessageProps {
  message: Message;
  index: number;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, index }) => {
  return (
    <div
      key={index}
      className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          message.role === 'user'
            ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white'
            : 'bg-gray-100 text-gray-800 border'
        } shadow-sm`}
      >
        {message.role === 'assistant' ? (
          <div className="prose prose-sm max-w-none">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        ) : (
          <p className="text-sm">{message.content}</p>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;

import React, { useState } from 'react';
import { toast } from 'sonner';
import ConversationSidebar from '@/components/ConversationSidebar';
import ChatArea from '@/components/ChatArea';
import AppHeader from '@/components/AppHeader';
import { useConversations } from '@/hooks/useConversations';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const Index = () => {
  const [prompt, setPrompt] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const {
    conversations,
    currentConversationId,
    setCurrentConversationId,
    createConversation,
    saveMessagesToConversation,
    loadConversationMessages,
    deleteConversation,
  } = useConversations();

  const sendPrompt = async () => {
    if (!prompt.trim() || loading) return;
    setLoading(true);

    const userMessage: Message = { role: 'user', content: prompt };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setPrompt('');

    try {
      console.log('Attempting to connect to backend...');
      console.log('URL:', 'https://group-7-d7dffvh0fydnbedj.southafricanorth-01.azurewebsites.net/api/prompt');
      console.log('Payload:', { prompt });

      const response = await fetch('https://group-7-d7dffvh0fydnbedj.southafricanorth-01.azurewebsites.net/api/prompt', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ prompt }),
      });

      console.log('Response status:', response.status);
      console.log('Response ok:', response.ok);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error response:', errorText);
        throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log('Response data:', data);

      const assistantMessage: Message = { role: 'assistant', content: data.response };
      const finalMessages = [...newMessages, assistantMessage];
      setMessages(finalMessages);

      if (currentConversationId) {
        await saveMessagesToConversation(currentConversationId, finalMessages);
      } else {
        const title = userMessage.content.slice(0, 50) + (userMessage.content.length > 50 ? '...' : '');
        const newConversationId = await createConversation(title);
        if (newConversationId) {
          setCurrentConversationId(newConversationId);
          await saveMessagesToConversation(newConversationId, finalMessages);
        }
      }

      toast.success('Response received!');
    } catch (error) {
      console.error('Detailed error connecting to backend:', error);

      let errorMessage = 'Error connecting to backend. ';

      if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
        errorMessage += 'This could be due to CORS issues, network connectivity, or the backend being offline.';
      } else if (error instanceof Error) {
        errorMessage += `Details: ${error.message}`;
      } else {
        errorMessage += 'Please check if the backend is running and accessible.';
      }

      const assistantErrorMessage: Message = { role: 'assistant', content: errorMessage };
      const finalMessages = [...newMessages, assistantErrorMessage];
      setMessages(finalMessages);
      toast.error('Failed to connect to backend');
    }

    setLoading(false);
  };

  const handleSelectConversation = async (conversationId: string) => {
    setCurrentConversationId(conversationId);
    const conversationMessages = await loadConversationMessages(conversationId);
    setMessages(conversationMessages);
    setSidebarOpen(false);
  };

  const handleNewConversation = () => {
    setCurrentConversationId(null);
    setMessages([]);
    setSidebarOpen(false);
  };

  const handleDeleteConversation = async (conversationId: string) => {
    await deleteConversation(conversationId);
    if (currentConversationId === conversationId) {
      handleNewConversation();
    }
  };

  return (
    <div className="h-screen flex w-full overflow-hidden">
      {/* Conversation Sidebar */}
      <ConversationSidebar
        conversations={conversations}
        currentConversationId={currentConversationId}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
        onDeleteConversation={handleDeleteConversation}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/* Main Content */}
      <div className={`flex-1 flex flex-col min-w-0 relative transition-all duration-300 ${
        sidebarOpen ? 'lg:ml-0' : 'lg:ml-0'
      }`}>
        {/* Mobile Header */}
        <AppHeader onToggleSidebar={() => setSidebarOpen(true)} />

        {/* Main Chat Area */}
        <ChatArea
          messages={messages}
          loading={loading}
          prompt={prompt}
          setPrompt={setPrompt}
          onSendPrompt={sendPrompt}
        />
      </div>
    </div>
  );
};

export default Index;

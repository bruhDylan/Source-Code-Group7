
import { useState, useEffect } from 'react';
import { supabase } from '@/integrations/supabase/client';
import { useAuth } from '@/contexts/AuthContext';
import { toast } from 'sonner';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export const useConversations = () => {
  const { user } = useAuth();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Fetch user's conversations
  const fetchConversations = async () => {
    if (!user) return;

    try {
      const { data, error } = await supabase
        .from('conversations')
        .select('*')
        .order('updated_at', { ascending: false });

      if (error) {
        console.error('Error fetching conversations:', error);
        return;
      }

      setConversations(data || []);
    } catch (error) {
      console.error('Error fetching conversations:', error);
    }
  };

  // Create a new conversation
  const createConversation = async (title: string): Promise<string | null> => {
    if (!user) return null;

    try {
      const { data, error } = await supabase
        .from('conversations')
        .insert({
          user_id: user.id,
          title: title.slice(0, 100), // Limit title length
        })
        .select()
        .single();

      if (error) {
        console.error('Error creating conversation:', error);
        toast.error('Failed to create conversation');
        return null;
      }

      await fetchConversations(); // Refresh the list
      return data.id;
    } catch (error) {
      console.error('Error creating conversation:', error);
      toast.error('Failed to create conversation');
      return null;
    }
  };

  // Save messages to a conversation
  const saveMessagesToConversation = async (conversationId: string, messages: Message[]) => {
    if (!user) return;

    try {
      // First, delete existing messages for this conversation
      await supabase
        .from('messages')
        .delete()
        .eq('conversation_id', conversationId);

      // Then insert new messages
      const messagesToInsert = messages.map(msg => ({
        conversation_id: conversationId,
        role: msg.role,
        content: msg.content,
      }));

      const { error } = await supabase
        .from('messages')
        .insert(messagesToInsert);

      if (error) {
        console.error('Error saving messages:', error);
        return;
      }

      // Update conversation timestamp
      await supabase
        .from('conversations')
        .update({ updated_at: new Date().toISOString() })
        .eq('id', conversationId);

      await fetchConversations(); // Refresh the list
    } catch (error) {
      console.error('Error saving messages:', error);
    }
  };

  // Load messages from a conversation
  const loadConversationMessages = async (conversationId: string): Promise<Message[]> => {
    try {
      const { data, error } = await supabase
        .from('messages')
        .select('*')
        .eq('conversation_id', conversationId)
        .order('created_at', { ascending: true });

      if (error) {
        console.error('Error loading messages:', error);
        return [];
      }

      return data.map(msg => ({
        role: msg.role as 'user' | 'assistant',
        content: msg.content,
      }));
    } catch (error) {
      console.error('Error loading messages:', error);
      return [];
    }
  };

  // Delete a conversation
  const deleteConversation = async (conversationId: string) => {
    try {
      const { error } = await supabase
        .from('conversations')
        .delete()
        .eq('id', conversationId);

      if (error) {
        console.error('Error deleting conversation:', error);
        toast.error('Failed to delete conversation');
        return;
      }

      toast.success('Conversation deleted');
      await fetchConversations();
      
      // If the deleted conversation was currently selected, clear it
      if (currentConversationId === conversationId) {
        setCurrentConversationId(null);
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
      toast.error('Failed to delete conversation');
    }
  };

  useEffect(() => {
    fetchConversations();
  }, [user]);

  return {
    conversations,
    currentConversationId,
    setCurrentConversationId,
    loading,
    fetchConversations,
    createConversation,
    saveMessagesToConversation,
    loadConversationMessages,
    deleteConversation,
  };
};

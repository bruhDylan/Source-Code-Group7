
import React from 'react';
import jsPDF from 'jspdf';
import { Download, Copy, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ExportButtonsProps {
  messages: Message[];
}

const ExportButtons: React.FC<ExportButtonsProps> = ({ messages }) => {
  const exportChatAsText = () => {
    const textContent = messages
      .map((msg) => `${msg.role === 'user' ? 'You' : 'AI'}: ${msg.content}`)
      .join('\n\n');

    const blob = new Blob([textContent], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'chat-export.txt';
    a.click();

    URL.revokeObjectURL(url);
    toast.success('Chat exported as TXT!');
  };

  const exportChatAsPDF = () => {
    const doc = new jsPDF();
    let y = 20;

    doc.setFontSize(16);
    doc.text('ThinkTank Chat Export', 10, 10);
    doc.setFontSize(12);

    messages.forEach((msg) => {
      const prefix = msg.role === 'user' ? 'You: ' : 'AI: ';
      const textLines = doc.splitTextToSize(prefix + msg.content, 180);
      
      if (y + textLines.length * 7 > 280) {
        doc.addPage();
        y = 20;
      }
      
      doc.text(textLines, 10, y);
      y += textLines.length * 7 + 10;
    });

    doc.save('thinktank-chat-export.pdf');
    toast.success('Chat exported as PDF!');
  };

  const copyChatToClipboard = () => {
    const textContent = messages
      .map((msg) => `${msg.role === 'user' ? 'You' : 'AI'}: ${msg.content}`)
      .join('\n\n');

    navigator.clipboard.writeText(textContent)
      .then(() => toast.success('Chat copied to clipboard!'))
      .catch(() => toast.error('Failed to copy chat'));
  };

  if (messages.length === 0) return null;

  return (
    <div className="px-6 pb-4 flex flex-wrap gap-2">
      <Button
        variant="outline"
        size="sm"
        onClick={exportChatAsText}
        className="flex items-center gap-2"
      >
        <FileText className="w-4 h-4" />
        Export TXT
      </Button>
      <Button
        variant="outline"
        size="sm"
        onClick={exportChatAsPDF}
        className="flex items-center gap-2"
      >
        <Download className="w-4 h-4" />
        Export PDF
      </Button>
      <Button
        variant="outline"
        size="sm"
        onClick={copyChatToClipboard}
        className="flex items-center gap-2"
      >
        <Copy className="w-4 h-4" />
        Copy Chat
      </Button>
    </div>
  );
};

export default ExportButtons;

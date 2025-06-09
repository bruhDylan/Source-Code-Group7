
import React from 'react';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/contexts/AuthContext';
import { User } from 'lucide-react';
import { toast } from 'sonner';

const UserMenu = () => {
  const { user: currentUser, signOut } = useAuth();

  const handleSignOut = async () => {
    try {
      await signOut();
      toast.success('Signed out successfully');
    } catch (error) {
      toast.error('Error signing out');
    }
  };

  if (!currentUser) {
    return null;
  }

  return (
    <div className="flex items-center gap-3">
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <User className="w-4 h-4" />
        <span>{currentUser.email}</span>
      </div>
      <Button
        variant="outline"
        size="sm"
        onClick={handleSignOut}
        className="text-sm"
      >
        Sign Out
      </Button>
    </div>
  );
};

export default UserMenu;

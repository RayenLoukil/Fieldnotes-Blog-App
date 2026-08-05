import React from 'react';
import { useUsers } from '@/hooks/useUsers';
import { useAuthStore } from '@/store/authStore';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Link } from 'react-router-dom';
import { Users, Mail, CheckCircle } from 'lucide-react';

export const UsersPage: React.FC = () => {
  const { useGetUsers } = useUsers();
  const { data: users, isLoading } = useGetUsers();
  const { currentUser, setCurrentUser } = useAuthStore();

  if (isLoading) return <div className="text-center py-8">Loading directory...</div>;

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 dark:border-zinc-800 pb-4">
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <Users className="h-8 w-8 text-steel-500" />
          <span>Active Authors</span>
        </h1>
        <p className="text-gray-500 dark:text-zinc-400 mt-1 text-sm">Select an author to view their profile, browse their technical notes, or switch mock accounts.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {users?.map((user) => {
          const isActiveSession = currentUser?.id === user.id;
          return (
            <Card key={user.id} className={`p-6 flex items-center justify-between border ${isActiveSession ? 'ring-2 ring-steel-500 border-transparent bg-steel-50/10' : ''}`}>
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-steel-100 text-steel-700 font-bold flex items-center justify-center text-sm shadow-inner">
                  {user.username.substring(0, 2).toUpperCase()}
                </div>
                <div>
                  <Link to={`/users/${user.id}`} className="font-bold text-gray-900 dark:text-zinc-100 hover:text-steel-500 hover:underline">
                    {user.username}
                  </Link>
                  <p className="text-xs text-gray-400 flex items-center gap-1 mt-0.5">
                    <Mail className="h-3 w-3" />
                    <span>{user.email}</span>
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                {isActiveSession ? (
                  <span className="inline-flex items-center gap-1 text-xs font-bold text-green-600 bg-green-50 dark:bg-green-950/20 px-2 py-1 rounded">
                    <CheckCircle className="h-3.5 w-3.5" />
                    <span>Active</span>
                  </span>
                ) : (
                  <Button 
                    size="sm" 
                    variant="ghost" 
                    onClick={() => setCurrentUser(user)}
                    className="text-xs"
                  >
                    Switch to user
                  </Button>
                )}
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};
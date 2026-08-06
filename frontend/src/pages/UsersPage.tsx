import React from 'react';
import { useUsers } from '@/hooks/useUsers';
import { Card } from '@/components/ui/Card';
import { Link } from 'react-router-dom';
import { Users, Mail } from 'lucide-react';

export const UsersPage: React.FC = () => {
  const { useGetUsers } = useUsers();
  const { data: users, isLoading } = useGetUsers();

  if (isLoading) return <div className="text-center py-8">Loading directory...</div>;

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 dark:border-zinc-800 pb-4">
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <Users className="h-8 w-8 text-steel-500" />
          <span>Authors</span>
        </h1>
        <p className="text-gray-500 dark:text-zinc-400 mt-1 text-sm">Browse registered authors and their notes.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {users?.map((user) => (
          <Card key={user.id} className="p-6 flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-steel-100 dark:bg-zinc-800 text-steel-700 dark:text-zinc-300 font-bold flex items-center justify-center text-sm shadow-inner">
              {user.username.substring(0, 2).toUpperCase()}
            </div>
            <div>
              <Link to={`/users/${user.id}`} className="font-bold text-gray-900 dark:text-zinc-100 hover:text-steel-500 hover:underline">
                {user.username}
              </Link>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
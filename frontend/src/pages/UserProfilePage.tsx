import React, { useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useUsers } from '@/hooks/useUsers';
import { usePosts } from '@/hooks/usePosts';
import { useAuthStore } from '@/store/authStore';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Dialog } from '@/components/ui/Dialog';
import { Input } from '@/components/ui/Input';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Terminal, Calendar, User as UserIcon, Settings, Trash, Edit } from 'lucide-react';

const profileUpdateSchema = z.object({
  username: z.string().min(3, "Username must be at least 3").max(50),
  email: z.string().email("Please enter a valid email"),
});

type ProfileFormInput = z.infer<typeof profileUpdateSchema>;

export const UserProfilePage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const userId = Number(id);
  const navigate = useNavigate();

  const { currentUser, logout } = useAuthStore();
  const { useGetUser, useUpdateUser, useDeleteUser } = useUsers();
  const { useGetPosts } = usePosts();

  const { data: user, isLoading: userLoading } = useGetUser(userId);
  const { data: posts, isLoading: postsLoading } = useGetPosts();
  const updateMutation = useUpdateUser(userId);
  const deleteMutation = useDeleteUser();

  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<ProfileFormInput>({
    resolver: zodResolver(profileUpdateSchema),
    values: user ? { username: user.username, email: user.email } : undefined,
  });

  if (userLoading || postsLoading) return <div className="animate-pulse bg-white p-6 rounded-lg h-64" />;
  if (!user) return <div className="text-center p-8">Author profile not found.</div>;

  // Fix: filter posts using nested relationship object IDs
  const userPosts = posts?.filter((p) => p.user?.id === userId) || [];
  const isMe = currentUser?.id === user.id;

  const onProfileUpdate = (data: ProfileFormInput) => {
    updateMutation.mutate(data, {
      onSuccess: () => {
        setIsSettingsOpen(false);
      }
    });
  };

  const onProfileDelete = () => {
    if (window.confirm("WARNING: Are you sure you want to delete your profile? This deletes all your note logs permanently!")) {
      deleteMutation.mutate(userId, {
        onSuccess: () => {
          logout();
          navigate('/signup');
        }
      });
    }
  };

  return (
    <div className="space-y-6">
      <Card className="p-6 bg-gradient-to-r from-steel-50/50 to-white dark:from-zinc-900/10 dark:to-zinc-900">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex flex-col sm:flex-row items-center gap-4 text-center sm:text-left">
            <div className="w-16 h-16 rounded-full bg-steel-500 text-white font-extrabold flex items-center justify-center text-2xl shadow-md border-2 border-white dark:border-zinc-800">
              {user.username.substring(0, 2).toUpperCase()}
            </div>
            <div>
              <h1 className="text-2xl font-bold flex items-center justify-center sm:justify-start gap-1">
                <UserIcon className="h-5 w-5 text-steel-500" />
                <span>{user.username}</span>
              </h1>
              <p className="text-xs text-gray-500 dark:text-zinc-400 mt-1">{user.email}</p>
              <p className="text-xs font-semibold text-steel-500 mt-2 bg-steel-100 dark:bg-zinc-800/80 px-2 py-0.5 rounded-full inline-block">
                {userPosts.length} Technical {userPosts.length === 1 ? 'Note' : 'Notes'} Published
              </p>
            </div>
          </div>

          {isMe && (
            <Button variant="secondary" size="sm" onClick={() => setIsSettingsOpen(true)} className="gap-1.5 self-center sm:self-start">
              <Settings className="h-4 w-4" />
              <span>Settings</span>
            </Button>
          )}
        </div>
      </Card>

      <div className="space-y-4">
        <h2 className="text-lg font-bold border-b border-gray-100 dark:border-zinc-800 pb-2">Logs Catalog</h2>
        {userPosts.length === 0 ? (
          <Card className="p-8 text-center text-gray-500">No notes written by this author yet.</Card>
        ) : (
          userPosts.map((post) => (
            <Card key={post.id} className="p-6">
              <div className="flex items-center gap-1.5 text-xs text-gray-500 dark:text-zinc-400 mb-2">
                <Calendar className="h-3 w-3" />
                <span>{new Date(post.created_at).toLocaleDateString()}</span>
              </div>
              <h3 className="text-lg font-bold mb-2">
                <Link to={`/posts/${post.id}`} className="text-gray-900 dark:text-zinc-100 hover:text-steel-500">
                  {post.title}
                </Link>
              </h3>
              <p className="text-gray-600 dark:text-zinc-300 text-sm line-clamp-3 leading-relaxed whitespace-pre-wrap">{post.content}</p>
              <div className="mt-3">
                <Link to={`/posts/${post.id}`} className="inline-flex items-center gap-1 text-xs font-bold text-steel-500 hover:underline">
                  <Terminal className="h-3.5 w-3.5" />
                  <span>Open detailed log</span>
                </Link>
              </div>
            </Card>
          ))
        )}
      </div>

      {isMe && (
        <Dialog isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} title="Account Settings">
          <form onSubmit={handleSubmit(onProfileUpdate)}>
            <Input label="Username" {...register('username')} error={errors.username?.message} />
            <Input label="Email address" {...register('email')} error={errors.email?.message} />

            <div className="flex items-center justify-between mt-6 pt-4 border-t border-gray-100 dark:border-zinc-800">
              <Button 
                type="button" 
                variant="danger" 
                className="gap-1 bg-red-100 hover:bg-red-200 text-red-700 dark:bg-red-950/20 dark:hover:bg-red-950/40 border border-transparent dark:text-red-400"
                onClick={onProfileDelete}
                isLoading={deleteMutation.isPending}
              >
                <Trash className="h-4 w-4" />
                <span>Delete Profile</span>
              </Button>
              
              <div className="flex gap-2">
                <Button type="button" variant="ghost" onClick={() => setIsSettingsOpen(false)}>Cancel</Button>
                <Button type="submit" isLoading={updateMutation.isPending}>Save changes</Button>
              </div>
            </div>
          </form>
        </Dialog>
      )}
    </div>
  );
};
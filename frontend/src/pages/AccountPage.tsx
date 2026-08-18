import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { useUsers } from '@/hooks/useUsers';
import { usePosts } from '@/hooks/usePosts';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Dialog } from '@/components/ui/Dialog';
import { Input } from '@/components/ui/Input';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Link } from 'react-router-dom';
import { User, Settings, Trash, Terminal, Calendar, Mail, Edit, Camera } from 'lucide-react';
import { API_ORIGIN } from '@/lib/api';

const profileUpdateSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3').max(50),
  email: z.string().email('Please enter a valid email'),
});

type ProfileFormInput = z.infer<typeof profileUpdateSchema>;

export const AccountPage: React.FC = () => {
  const navigate = useNavigate();
  const { currentUser, logout, checkAuth } = useAuthStore();
  const { useUpdateUser, useDeleteUser, useUploadPicture } = useUsers();
  const { useGetUserPosts } = usePosts();

  const { data: myPosts = [] } = useGetUserPosts(currentUser!.id);

  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  // Only runs if currentUser exists (guaranteed by ProtectedRoute)
  const updateMutation = useUpdateUser(currentUser!.id);
  const deleteMutation = useDeleteUser();
  const uploadMutation = useUploadPicture(currentUser!.id);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const MAX_SIZE_BYTES = 5 * 1024 * 1024;

  const onFileSelected = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    e.target.value = '';
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      alert('Please select an image file.');
      return;
    }
    if (file.size > MAX_SIZE_BYTES) {
      alert('Image must be smaller than 5MB.');
      return;
    }

    uploadMutation.mutate(file);
  };

  // Form always seeded from currentUser (UserPrivate — has email)
  const { register, handleSubmit, formState: { errors } } = useForm<ProfileFormInput>({
    resolver: zodResolver(profileUpdateSchema),
    values: {
      username: currentUser!.username,
      email: currentUser!.email,
    },
  });



  const onProfileUpdate = (data: ProfileFormInput) => {
    updateMutation.mutate(data, {
      onSuccess: async () => {
        await checkAuth(); // re-fetch /me so authStore.currentUser reflects new username/email immediately
        setIsSettingsOpen(false);
      },
    });
  };

  const onProfileDelete = () => {
    if (window.confirm('WARNING: This permanently deletes your account and all your posts.')) {
      deleteMutation.mutate(currentUser!.id, {
        onSuccess: () => {
          logout();
          navigate('/signup');
        },
      });
    }
  };

  if (!currentUser) return null; // ProtectedRoute handles this, just a safety guard

  return (
    <div className="space-y-6">

      {/* Profile Header Card */}
      <Card className="p-6">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex flex-col sm:flex-row items-center gap-4 text-center sm:text-left">
            <div className="w-16 h-16 rounded-full overflow-hidden shadow-md border-2 border-white dark:border-zinc-800">
              <img
                src={`${API_ORIGIN}${currentUser.image_path}`}
                alt={currentUser.username}
                className="w-full h-full object-cover"
              />
            </div>
            <div>
              <h1 className="text-2xl font-bold flex items-center justify-center sm:justify-start gap-1">
                <User className="h-5 w-5 text-steel-500" />
                <span>{currentUser.username}</span>
              </h1>
              {/* Email shows correctly because currentUser comes from /me (UserPrivate) */}
              <p className="text-xs text-gray-500 dark:text-zinc-400 flex items-center gap-1 mt-1">
                <Mail className="h-3 w-3" />
                <span>{currentUser.email}</span>
              </p>
              <p className="text-xs font-semibold text-steel-500 mt-2 bg-steel-100 dark:bg-zinc-800/80 px-2 py-0.5 rounded-full inline-block">
                {myPosts.length} {myPosts.length === 1 ? 'Note' : 'Notes'} Published
              </p>
            </div>
          </div>

          <Button
            variant="secondary"
            size="sm"
            onClick={() => setIsSettingsOpen(true)}
            className="gap-1.5 self-center sm:self-start"
          >
            <Settings className="h-4 w-4" />
            <span>Edit Profile</span>
          </Button>
        </div>
      </Card>

      {/* My Posts */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold border-b border-gray-100 dark:border-zinc-800 pb-2">
          My Notes
        </h2>

        {myPosts.length === 0 ? (
          <Card className="p-8 text-center text-gray-500">
            You haven't written any notes yet.
          </Card>
        ) : (
          myPosts.map((post) => (
            <Card key={post.id} className="p-6">
              <div className="flex items-center gap-1.5 text-xs text-gray-500 dark:text-zinc-400 mb-2">
                <Calendar className="h-3 w-3" />
                <span>{new Date(post.created_at).toLocaleDateString()}</span>
              </div>
              <h3 className="text-lg font-bold mb-2">
                <Link
                  to={`/posts/${post.id}`}
                  className="text-gray-900 dark:text-zinc-100 hover:text-steel-500"
                >
                  {post.title}
                </Link>
              </h3>
              <p className="text-gray-600 dark:text-zinc-300 text-sm line-clamp-3 leading-relaxed whitespace-pre-wrap">
                {post.content}
              </p>
              <div className="mt-3 flex items-center gap-3">
                <Link
                  to={`/posts/${post.id}`}
                  className="inline-flex items-center gap-1 text-xs font-bold text-steel-500 hover:underline"
                >
                  <Terminal className="h-3.5 w-3.5" />
                  <span>Open</span>
                </Link>
                <Link
                  to={`/posts/${post.id}`}
                  className="inline-flex items-center gap-1 text-xs font-bold text-gray-400 hover:text-steel-500 hover:underline"
                >
                  <Edit className="h-3.5 w-3.5" />
                  <span>Edit</span>
                </Link>
              </div>
            </Card>
          ))
        )}
      </div>

      {/* Account Settings Dialog */}
      <Dialog
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        title="Account Settings"
      >
        <div className="flex flex-col items-center mb-6">
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="relative group w-20 h-20 rounded-full overflow-hidden border-2 border-white dark:border-zinc-800 shadow-md"
            disabled={uploadMutation.isPending}
          >
            <img
              src={`${API_ORIGIN}${currentUser!.image_path}`}
              alt={currentUser!.username}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
              <Camera className="h-6 w-6 text-white" />
            </div>
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={onFileSelected}
          />
          {uploadMutation.isPending && (
            <p className="text-xs text-gray-500 mt-2">Uploading...</p>
          )}
          {uploadMutation.isError && (
            <p className="text-xs text-red-500 mt-2">
              {(uploadMutation.error as any)?.error?.message || 'Upload failed. Try a different image.'}
            </p>
          )}
        </div>
        <form onSubmit={handleSubmit(onProfileUpdate)}>
          <Input
            label="Username"
            {...register('username')}
            error={errors.username?.message}
          />
          <Input
            label="Email address"
            type="email"
            {...register('email')}
            error={errors.email?.message}
          />

          <div className="flex items-center justify-between mt-6 pt-4 border-t border-gray-100 dark:border-zinc-800">
            <Button
              type="button"
              variant="danger"
              className="gap-1"
              onClick={onProfileDelete}
              isLoading={deleteMutation.isPending}
            >
              <Trash className="h-4 w-4" />
              <span>Delete Account</span>
            </Button>

            <div className="flex gap-2">
              <Button type="button" variant="ghost" onClick={() => setIsSettingsOpen(false)}>
                Cancel
              </Button>
              <Button type="submit" isLoading={updateMutation.isPending}>
                Save Changes
              </Button>
            </div>
          </div>
        </form>
      </Dialog>
    </div>
  );
};
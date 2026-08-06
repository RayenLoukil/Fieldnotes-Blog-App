import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAuthStore } from '@/store/authStore';
import { usePosts } from '@/hooks/usePosts';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

import { Navbar } from '@/components/Navbar';
import { ProtectedRoute } from '@/components/ProtectedRoute';
import { Dialog } from '@/components/ui/Dialog';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Button } from '@/components/ui/Button';

import { FeedPage } from '@/pages/FeedPage';
import { PostDetailPage } from '@/pages/PostDetailPage';
import { UserProfilePage } from '@/pages/UserProfilePage';
import { UsersPage } from '@/pages/UsersPage';
import { LoginPage } from '@/pages/LoginPage';
import { RegisterPage } from '@/pages/RegisterPage';

import { AccountPage } from '@/pages/AccountPage';

const queryClient = new QueryClient({
  defaultOptions: { queries: { refetchOnWindowFocus: false, retry: 1 } },
});

const createPostSchema = z.object({
  title: z.string().min(3).max(100),
  content: z.string().min(10),
});
type CreatePostInput = z.infer<typeof createPostSchema>;

const AppContent: React.FC = () => {
  const [isWriteOpen, setIsWriteOpen] = useState(false);
  const { currentUser, isAuthenticated, isInitializing, checkAuth } = useAuthStore();
  const { useCreatePost } = usePosts();
  const createMutation = useCreatePost();

  // Validate the stored token (if any) once, when the app first mounts
  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const { register, handleSubmit, reset, formState: { errors } } = useForm<CreatePostInput>({
    resolver: zodResolver(createPostSchema),
  });

  const onCreatePostSubmit = (data: CreatePostInput) => {
    if (!currentUser) return;
    createMutation.mutate(
      { title: data.title, content: data.content, id_user: currentUser.id },
      { onSuccess: () => { setIsWriteOpen(false); reset(); } }
    );
  };

  // Don't render routes until we know whether the user is really authenticated
  if (isInitializing) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#fafafa] dark:bg-[#1a1a1a]">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-[#fafafa] dark:bg-[#1a1a1a] flex flex-col transition-colors duration-200">
        <Navbar onCreatePostClick={() => setIsWriteOpen(true)} />

        <main className="flex-grow max-w-4xl w-full mx-auto px-4 pt-24 pb-16">
          <Routes>
            <Route path="/login" element={isAuthenticated ? <Navigate to="/" replace /> : <LoginPage />} />
            <Route path="/signup" element={isAuthenticated ? <Navigate to="/" replace /> : <RegisterPage />} />

            <Route path="/" element={<ProtectedRoute><FeedPage /></ProtectedRoute>} />
            <Route path="/posts/:id" element={<ProtectedRoute><PostDetailPage /></ProtectedRoute>} />
            <Route path="/users/:id" element={<ProtectedRoute><UserProfilePage /></ProtectedRoute>} />
            <Route path="/users" element={<ProtectedRoute><UsersPage /></ProtectedRoute>} />

            <Route path="*" element={<Navigate to="/" replace />} />
            <Route path="/account" element={<ProtectedRoute><AccountPage /></ProtectedRoute>} />

          </Routes>
        </main>

        {isAuthenticated && (
          <Dialog isOpen={isWriteOpen} onClose={() => setIsWriteOpen(false)} title="Write a Technical Note">
            <form onSubmit={handleSubmit(onCreatePostSubmit)}>
              <div className="bg-gray-50 dark:bg-zinc-900 border border-gray-100 dark:border-zinc-800 p-3 rounded text-xs mb-4">
                Posting as: <strong className="text-steel-500">{currentUser?.username}</strong>
              </div>
              <Input label="Log Entry Title" {...register('title')} error={errors.title?.message} />
              <Textarea label="Content" rows={8} {...register('content')} error={errors.content?.message} />
              <div className="flex items-center justify-end gap-2 mt-4 pt-4 border-t border-gray-100 dark:border-zinc-800">
                <Button type="button" variant="ghost" onClick={() => setIsWriteOpen(false)}>Cancel</Button>
                <Button type="submit" isLoading={createMutation.isPending}>Publish</Button>
              </div>
            </form>
          </Dialog>
        )}
      </div>
    </BrowserRouter>
  );
};

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}


// inside <Routes>:

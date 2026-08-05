import React, { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { usePosts } from '@/hooks/usePosts';
import { useAuthStore } from '@/store/authStore';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Dialog } from '@/components/ui/Dialog';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Calendar, Trash2, Edit, ArrowLeft, Terminal } from 'lucide-react';

const updateSchema = z.object({
  title: z.string().min(3, "Title must be at least 3 characters").max(100),
  content: z.string().min(10, "Content must contain at least 10 characters"),
});

type UpdateFormInput = z.infer<typeof updateSchema>;

export const PostDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const postId = Number(id);

  const { currentUser } = useAuthStore();
  const { useGetPost, useUpdatePost, useDeletePost } = usePosts();
  
  const { data: post, isLoading, error } = useGetPost(postId);
  const updateMutation = useUpdatePost(postId);
  const deleteMutation = useDeletePost();

  const [isEditOpen, setIsEditOpen] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<UpdateFormInput>({
    resolver: zodResolver(updateSchema),
    values: post ? { title: post.title, content: post.content } : undefined,
  });

  const onUpdateSubmit = (data: UpdateFormInput) => {
    updateMutation.mutate(data, {
      onSuccess: () => {
        setIsEditOpen(false);
      }
    });
  };

  const onDelete = () => {
    if (window.confirm("Are you sure you want to delete this log entry?")) {
      deleteMutation.mutate(postId, {
        onSuccess: () => navigate('/')
      });
    }
  };

  if (isLoading) return <div className="animate-pulse bg-white p-6 rounded-lg h-64" />;
  if (error || !post) return <div className="text-center p-8">Log entry not found.</div>;

  // Use the nested user.id relationship to check ownership
  const isAuthor = currentUser?.id === post.user?.id;

  return (
    <div className="space-y-4">
      <button onClick={() => navigate(-1)} className="inline-flex items-center gap-1.5 text-xs font-bold text-gray-500 hover:text-steel-500 transition-colors">
        <ArrowLeft className="h-4 w-4" />
        <span>Back to feed</span>
      </button>

      <Card className="p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-gray-100 dark:border-zinc-800 pb-4 mb-4">
          <div className="flex items-center gap-4">
            <Link to={`/users/${post.user?.id}`}>
              <div className="w-12 h-12 rounded-full bg-steel-100 dark:bg-zinc-800 text-steel-700 dark:text-steel-300 font-extrabold flex items-center justify-center text-sm shadow-inner border border-gray-100">
                {post.user?.username.substring(0, 2).toUpperCase()}
              </div>
            </Link>
            <div>
              <div>
                <Link to={`/users/${post.user?.id}`} className="font-bold text-steel-500 hover:underline">
                  {post.user?.username}
                </Link>
              </div>
              <p className="text-xs text-gray-500 flex items-center gap-1 mt-0.5">
                <Calendar className="h-3 w-3" />
                {new Date(post.created_at).toLocaleDateString(undefined, {
                  weekday: 'long',
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </p>
            </div>
          </div>

          {isAuthor && (
            <div className="flex items-center gap-2 self-end md:self-auto">
              <Button size="sm" variant="secondary" onClick={() => setIsEditOpen(true)} className="gap-1">
                <Edit className="h-3.5 w-3.5" />
                <span>Edit</span>
              </Button>
              <Button size="sm" variant="danger" onClick={onDelete} className="gap-1" isLoading={deleteMutation.isPending}>
                <Trash2 className="h-3.5 w-3.5" />
                <span>Delete</span>
              </Button>
            </div>
          )}
        </div>

        <h1 className="text-2xl md:text-3xl font-extrabold text-gray-900 dark:text-zinc-100 mb-6 flex items-start gap-2">
          <Terminal className="h-7 w-7 text-steel-500 mt-1 flex-shrink-0" />
          <span>{post.title}</span>
        </h1>

        <div className="text-gray-700 dark:text-zinc-200 text-sm leading-relaxed whitespace-pre-wrap font-sans bg-gray-50/50 dark:bg-zinc-950/20 p-4 border border-gray-100 dark:border-zinc-800/80 rounded-md">
          {post.content}
        </div>
      </Card>

      <Dialog isOpen={isEditOpen} onClose={() => setIsEditOpen(false)} title="Edit Note Details">
        <form onSubmit={handleSubmit(onUpdateSubmit)}>
          <Input label="Title" {...register('title')} error={errors.title?.message} />
          <Textarea label="Content / Console payload" rows={8} {...register('content')} error={errors.content?.message} />
          <div className="flex items-center justify-end gap-2 mt-4 pt-4 border-t border-gray-100 dark:border-zinc-800">
            <Button type="button" variant="ghost" onClick={() => setIsEditOpen(false)}>Cancel</Button>
            <Button type="submit" isLoading={updateMutation.isPending}>Save Changes</Button>
          </div>
        </form>
      </Dialog>
    </div>
  );
};
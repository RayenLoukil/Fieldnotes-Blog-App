import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Post, PostCreate, PostUpdate } from '@/types/api';

export const usePosts = () => {
  const queryClient = useQueryClient();

  const useGetPosts = () => useQuery<Post[]>({
    queryKey: ['posts'],
    queryFn: async () => {
      const { data } = await api.get<Post[]>('/posts');
      return data;
    },
  });

  const useGetPost = (id: number) => useQuery<Post>({
    queryKey: ['posts', id],
    queryFn: async () => {
      const { data } = await api.get<Post>(`/posts/${id}`);
      return data;
    },
    enabled: !isNaN(id) && id > 0,
  });

  const useCreatePost = () => useMutation({
    mutationFn: async (payload: PostCreate) => {
      const { data } = await api.post<Post>('/posts', payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });

  const useUpdatePost = (id: number) => useMutation({
    mutationFn: async (payload: PostUpdate) => {
      const { data } = await api.patch<Post>(`/posts/${id}`, payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      queryClient.invalidateQueries({ queryKey: ['posts', id] });
    },
  });

  const useDeletePost = () => useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/posts/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });

  return {
    useGetPosts,
    useGetPost,
    useCreatePost,
    useUpdatePost,
    useDeletePost,
  };
};
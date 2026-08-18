import { useQuery, useMutation, useQueryClient, useInfiniteQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Post, PostCreate, PostUpdate, PaginatedPosts } from '@/types/api';

export const usePosts = () => {
  const queryClient = useQueryClient();

  const useGetPosts = () => useQuery<Post[]>({
    queryKey: ['posts'],
    queryFn: async () => {
      const { data } = await api.get<PaginatedPosts>('/posts', {
        params: { skip: 0, limit: 100 },
      });
      return data.posts;
    },
  });

  const POSTS_PER_PAGE = 10;

  const useGetPostsInfinite = () => useInfiniteQuery({
    queryKey: ['posts', 'infinite'],
    queryFn: async ({ pageParam = 0 }) => {
      const { data } = await api.get<PaginatedPosts>('/posts', {
        params: { skip: pageParam, limit: POSTS_PER_PAGE },
      });
      return data;
    },
    initialPageParam: 0,
    getNextPageParam: (lastPage) => {
      if (!lastPage.has_more) return undefined;
      return lastPage.skip + lastPage.limit;
    },
  });


  const useGetUserPosts = (userId: number) => useQuery<Post[]>({
    queryKey: ['posts', 'user', userId],
    queryFn: async () => {
      const { data } = await api.get<PaginatedPosts>(`/users/${userId}/posts`, {
        params: { skip: 0, limit: 100 },
      });
      return data.posts;
    },
    enabled: !isNaN(userId) && userId > 0,
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
    useGetPostsInfinite,
    useGetUserPosts,
    useGetPost,
    useCreatePost,
    useUpdatePost,
    useDeletePost,
  };
};
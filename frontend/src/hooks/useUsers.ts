import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { User, UserUpdate } from '@/types/api';
import { useAuthStore } from '@/store/authStore';

export const useUsers = () => {
  const queryClient = useQueryClient();
  const updateProfileState = useAuthStore((state) => state.updateProfileState);

  const useGetUsers = () => useQuery<User[]>({
    queryKey: ['users'],
    queryFn: async () => {
      const { data } = await api.get<User[]>('/users');
      return data;
    },
  });

  const useGetUser = (id: number) => useQuery<User>({
    queryKey: ['users', id],
    queryFn: async () => {
      const { data } = await api.get<User>(`/users/${id}`);
      return data;
    },
    enabled: !isNaN(id) && id > 0,
  });

  const useUpdateUser = (id: number) => useMutation({
    mutationFn: async (payload: UserUpdate) => {
      const { data } = await api.patch<User>(`/users/${id}`, payload);
      return data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      queryClient.invalidateQueries({ queryKey: ['users', id] });
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      // Sync update with active auth store state if editing oneself
      updateProfileState(data);
    },
  });

  const useDeleteUser = () => useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/users/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });

  return {
    useGetUsers,
    useGetUser,
    useUpdateUser,
    useDeleteUser,
  };
};
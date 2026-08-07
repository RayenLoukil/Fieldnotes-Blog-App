import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { UserPublic, UserPrivate, UserUpdate } from '@/types/api';
import { useAuthStore } from '@/store/authStore';

export const useUsers = () => {
  const queryClient = useQueryClient();
  const updateProfileState = useAuthStore((state) => state.updateProfileState);

  const useGetUsers = () => useQuery<UserPublic[]>({
    queryKey: ['users'],
    queryFn: async () => {
      const { data } = await api.get<UserPublic[]>('/users');
      return data;
    },
  });

  const useGetUser = (id: number) => useQuery<UserPublic>({
    queryKey: ['users', id],
    queryFn: async () => {
      const { data } = await api.get<UserPublic>(`/users/${id}`);
      return data;
    },
    enabled: !isNaN(id) && id > 0,
  });

  const useUpdateUser = (id: number) => useMutation({
    mutationFn: async (payload: UserUpdate) => {
      const { data } = await api.patch<UserPrivate>(`/users/${id}`, payload);
      return data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      queryClient.invalidateQueries({ queryKey: ['users', id] });
      queryClient.invalidateQueries({ queryKey: ['posts'] });
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


const useUploadPicture = (id: number) => useMutation({
  mutationFn: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const { data } = await api.patch<UserPrivate>(`/users/${id}/picture`, formData);
    return data;
  },
  onSuccess: (data) => {
    queryClient.invalidateQueries({ queryKey: ['users'] });
    queryClient.invalidateQueries({ queryKey: ['users', id] });
    queryClient.invalidateQueries({ queryKey: ['posts'] });
    updateProfileState(data);
  },
});


  return {
    useGetUsers,
    useGetUser,
    useUpdateUser,
    useDeleteUser,
    useUploadPicture 
  };
};



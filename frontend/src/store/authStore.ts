import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User } from '@/types/api';
import { api } from '@/lib/api';

interface AuthState {
  currentUser: User | null;
  isAuthenticated: boolean;
  login: (username: string) => Promise<void>;
  signup: (username: string, email: string) => Promise<User>;
  updateProfileState: (updatedUser: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      currentUser: null,
      isAuthenticated: false,

      login: async (username: string) => {
        try {
          // Fetch existing users to verify the account
          const { data: users } = await api.get<User[]>('/users');
          const matchedUser = users.find(
            (u) => u.username.toLowerCase() === username.toLowerCase()
          );

          if (!matchedUser) {
            throw new Error("Username not found. Please register first.");
          }

          set({ currentUser: matchedUser, isAuthenticated: true });
        } catch (error: any) {
          const errMsg = error?.response?.data?.error?.message || error.message || "Login failed";
          throw new Error(errMsg);
        }
      },

      signup: async (username: string, email: string) => {
        try {
          const { data: newUser } = await api.post<User>('/users', { username, email });
          set({ currentUser: newUser, isAuthenticated: true });
          return newUser;
        } catch (error: any) {
          const errMsg = error?.response?.data?.error?.message || "Registration failed";
          throw new Error(errMsg);
        }
      },

      updateProfileState: (updatedUser: User) => {
        set({ currentUser: updatedUser });
      },

      logout: () => {
        set({ currentUser: null, isAuthenticated: false });
      },
    }),
    {
      name: 'fieldnotes-auth-session',
    }
  )
);
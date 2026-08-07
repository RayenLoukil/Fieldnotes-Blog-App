import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { UserPrivate } from '@/types/api';
import { api } from '@/lib/api';

interface AuthState {
  token: string | null;
  currentUser: UserPrivate | null;
  isAuthenticated: boolean;
  isInitializing: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
  updateProfileState: (user: UserPrivate) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      currentUser: null,
      isAuthenticated: false,
      isInitializing: true,

      login: async (email: string, password: string) => {
        // The backend expects OAuth2PasswordRequestForm: form-urlencoded, NOT JSON
        const params = new URLSearchParams();
        params.append('username', email); // backend treats "username" field as email
        params.append('password', password);

        const { data } = await api.post('/users/token', params, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });

        set({ token: data.access_token });
        await get().checkAuth(); // fetch and store the real user object
      },

      register: async (username: string, email: string, password: string) => {
        await api.post('/users', { username, email, password }); // this one IS JSON
        await get().login(email, password); // auto-login right after registering
      },

      logout: () => {
        set({ token: null, currentUser: null, isAuthenticated: false });
      },

      checkAuth: async () => {
        const token = get().token;
        if (!token) {
          set({ isAuthenticated: false, currentUser: null, isInitializing: false });
          return;
        }
        try {
          const { data } = await api.get<UserPrivate>('/users/me');
          set({ currentUser: data, isAuthenticated: true, isInitializing: false });
        } catch {
          // token exists but is expired/invalid — clear everything
          set({ token: null, currentUser: null, isAuthenticated: false, isInitializing: false });
        }
      },

      updateProfileState: (user: UserPrivate) => {
        set({ currentUser: user });
      },
    }),
    {
      name: 'fieldnotes-auth',
      partialize: (state) => ({ token: state.token }), // ONLY persist the token, not currentUser
    }
  )
);
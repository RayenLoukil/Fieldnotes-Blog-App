export interface User {
  id: number;
  username: string;
  email: string;
}

export interface Post {
  id: number;
  title: string;
  content: string;
  created_at: string;
  user: User; // Nested relationship
}

export interface UserCreate {
  username: string;
  email: string;
}

export interface UserUpdate {
  username?: string;
  email?: string;
}

export interface PostCreate {
  title: string;
  content: string;
}

export interface PostUpdate {
  title?: string;
  content?: string;
}

export interface ApiError {
  error: {
    message: string;
    status_code: number;
    details?: Array<{
      loc: Array<string | number>;
      msg: string;
      type: string;
    }>;
  };
}
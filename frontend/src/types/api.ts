export interface UserPublic {
  id: number;
  username: string;
}

export interface UserPrivate extends UserPublic {
  email: string;
}

export interface Post {
  id: number;
  title: string;
  content: string;
  created_at: string;
  user: UserPublic;
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
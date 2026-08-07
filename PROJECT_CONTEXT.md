
# PROJECT CONTEXT

Generated:
2026-08-07 13:32:39.234867

Purpose:
This document contains the complete source code
of the project for AI assistance.

AI ROLE:

Act as a senior developer mentor.

Do not automatically rewrite everything.

Explain:
- architecture
- problems
- possible solutions
- reasoning

Then suggest code for me to implement.

# PROJECT STRUCTURE

- .\database.py
- .\frontend\package.json
- .\main.py
- .\models.py
- .\readme.md
- .\schemas.py
- .\auth.py
- .\config.py
- .\frontend\index.html
- .\frontend\postcss.config.js
- .\frontend\src\App.tsx
- .\frontend\src\components\Navbar.tsx
- .\frontend\src\components\ProtectedRoute.tsx
- .\frontend\src\components\ui\Button.tsx
- .\frontend\src\components\ui\Card.tsx
- .\frontend\src\components\ui\Dialog.tsx
- .\frontend\src\components\ui\Input.tsx
- .\frontend\src\components\ui\Textarea.tsx
- .\frontend\src\hooks\usePosts.ts
- .\frontend\src\hooks\useUsers.ts
- .\frontend\src\index.css
- .\frontend\src\lib\api.ts
- .\frontend\src\main.tsx
- .\frontend\src\pages\AccountPage.tsx
- .\frontend\src\pages\FeedPage.tsx
- .\frontend\src\pages\LoginPage.tsx
- .\frontend\src\pages\PostDetailPage.tsx
- .\frontend\src\pages\RegisterPage.tsx
- .\frontend\src\pages\UserProfilePage.tsx
- .\frontend\src\pages\UsersPage.tsx
- .\frontend\src\store\authStore.ts
- .\frontend\src\types\api.ts
- .\frontend\src\vite-env.d.ts
- .\frontend\tailwind.config.js
- .\frontend\tsconfig.json
- .\frontend\tsconfig.node.json
- .\frontend\vite.config.ts
- .\router\__init__.py
- .\router\posts.py
- .\router\users.py


# PROJECT FILES


================================================================================
# FILE: .\database.py
================================================================================

```py
0001 | from sqlalchemy import create_engine
0002 | from sqlalchemy.orm import DeclarativeBase , sessionmaker
0003 | 
0004 | DB_URL = "sqlite:///./fieldnotes.db"
0005 | 
0006 | engine = create_engine(
0007 |     DB_URL,
0008 |     connect_args={"check_same_thread": False},)
0009 | 
0010 | SessionLocal  = sessionmaker(autocommit=False , bind=engine , autoflush=False )
0011 | 
0012 | class Base(DeclarativeBase):
0013 |     pass
0014 | 
0015 | def get_db():
0016 |     with SessionLocal() as db :
0017 |         yield db

```


================================================================================
# FILE: .\frontend\package.json
================================================================================

```json
0001 | {
0002 |   "name": "fieldnotes-frontend",
0003 |   "private": true,
0004 |   "version": "1.0.0",
0005 |   "type": "module",
0006 |   "scripts": {
0007 |     "dev": "vite",
0008 |     "build": "tsc && vite build",
0009 |     "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
0010 |     "preview": "vite preview"
0011 |   },
0012 |   "dependencies": {
0013 |     "@hookform/resolvers": "^3.10.0",
0014 |     "@tanstack/react-query": "^5.101.4",
0015 |     "axios": "^1.19.0",
0016 |     "lucide-react": "^0.468.0",
0017 |     "react": "^18.3.1",
0018 |     "react-dom": "^18.3.1",
0019 |     "react-hook-form": "^7.84.0",
0020 |     "react-router-dom": "^6.30.4",
0021 |     "zod": "^3.25.76",
0022 |     "zustand": "^5.0.14"
0023 |   },
0024 |   "devDependencies": {
0025 |     "@types/node": "^26.1.2",
0026 |     "@types/react": "^18.3.12",
0027 |     "@types/react-dom": "^18.3.1",
0028 |     "@vitejs/plugin-react": "^4.7.0",
0029 |     "autoprefixer": "^10.5.4",
0030 |     "postcss": "^8.5.25",
0031 |     "tailwindcss": "^3.4.19",
0032 |     "typescript": "^5.6.3",
0033 |     "vite": "^5.4.11"
0034 |   }
0035 | }

```


================================================================================
# FILE: .\main.py
================================================================================

```py
0001 | from fastapi import FastAPI, status, Request
0002 | from fastapi.middleware.cors import CORSMiddleware
0003 | from fastapi.responses import JSONResponse
0004 | from fastapi.exceptions import RequestValidationError
0005 | from starlette.exceptions import HTTPException as StarletteHTTPException
0006 | 
0007 | # database
0008 | from database import engine, Base
0009 | 
0010 | # routers
0011 | from router import posts, users  
0012 | 
0013 | ## Create the database tables
0014 | Base.metadata.create_all(bind=engine)
0015 | 
0016 | ## Initialize the FastAPI app
0017 | app = FastAPI(
0018 |     title="Fieldnotes API",
0019 |     description="A pure JSON Blog API for posting about tech and sharing knowledge",
0020 |     version="1.0.0",
0021 | )
0022 | 
0023 | # ---------------------------------------------------------
0024 | # CORS configuration (Allows React dev server to communicate)
0025 | # ---------------------------------------------------------
0026 | origins = [
0027 |     "http://localhost:5173",  # Vite Dev Server
0028 |     "http://127.0.0.1:5173",
0029 | ]
0030 | 
0031 | app.add_middleware(
0032 |     CORSMiddleware,
0033 |     allow_origins=origins,
0034 |     allow_credentials=True,
0035 |     allow_methods=["*"],
0036 |     allow_headers=["*"],
0037 | )
0038 | 
0039 | 
0040 | @app.get("/api/health", tags=["System"])
0041 | def health_check():
0042 |     return {"status": "healthy", "message": "Fieldnotes API is fully operational"}
0043 | 
0044 | 
0045 | # Include API Routers
0046 | app.include_router(users.router, prefix="/api/users", tags=["Users"])
0047 | app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])
0048 | 
0049 | 
0050 | # ---------------------------------------------------------
0051 | # Global JSON Exception Handlers
0052 | # ---------------------------------------------------------
0053 | 
0054 | @app.exception_handler(StarletteHTTPException)
0055 | def http_exception_handler(request: Request, exception: StarletteHTTPException):
0056 |     return JSONResponse(
0057 |         status_code=exception.status_code,
0058 |         content={
0059 |             "error": {
0060 |                 "message": exception.detail,
0061 |                 "status_code": exception.status_code
0062 |             }
0063 |         }
0064 |     )
0065 | 
0066 | 
0067 | @app.exception_handler(RequestValidationError)
0068 | def validation_exception_handler(request: Request, exception: RequestValidationError):
0069 |     return JSONResponse(
0070 |         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
0071 |         content={
0072 |             "error": {
0073 |                 "message": "Validation failed",
0074 |                 "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
0075 |                 "details": exception.errors()
0076 |             }
0077 |         }
0078 |     )
0079 | 
0080 | 
0081 | @app.exception_handler(Exception)
0082 | def global_exception_handler(request: Request, exception: Exception):
0083 |     # In production, log this exception details to terminal/logs
0084 |     return JSONResponse(
0085 |         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
0086 |         content={
0087 |             "error": {
0088 |                 "message": "Internal server error",
0089 |                 "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
0090 |             }
0091 |         }
0092 |     )

```


================================================================================
# FILE: .\models.py
================================================================================

```py
0001 | from __future__ import annotations
0002 | from sqlalchemy import Integer , String , Text , DateTime, ForeignKey
0003 | from sqlalchemy.orm import Mapped , mapped_column, relationship
0004 | from database import Base
0005 | from datetime import datetime, UTC
0006 | 
0007 | class Post(Base):
0008 |     __tablename__ = "posts"
0009 |     
0010 |     id : Mapped[int] = mapped_column (Integer , primary_key=True , index=True)
0011 |     title:Mapped[str] = mapped_column(String(100) , nullable=False)
0012 |     content:Mapped[str] = mapped_column(Text , nullable=False)
0013 |     id_user : Mapped[int] = mapped_column (Integer, ForeignKey("users.id") , nullable=False, index=True)
0014 |     created_at :Mapped[datetime] = mapped_column(DateTime(timezone=True) , default=lambda: datetime.now(UTC))
0015 |     user : Mapped[User] = relationship(back_populates="posts")
0016 |     
0017 |     
0018 | class User(Base):
0019 |     __tablename__ = "users"
0020 |     
0021 |     id : Mapped[int] = mapped_column (Integer , primary_key=True , index=True)
0022 |     username : Mapped[str] = mapped_column (String(50) , unique=True)
0023 |     email : Mapped[str] = mapped_column (String(100) , unique=True)
0024 |     
0025 |     password_hash : Mapped[str] = mapped_column (String(200) , nullable=False)
0026 |     
0027 |     
0028 |     
0029 | 
0030 |     posts : Mapped[list[Post]] = relationship(back_populates="user" , cascade="all, delete-orphan")

```


================================================================================
# FILE: .\readme.md
================================================================================

```md

```


================================================================================
# FILE: .\schemas.py
================================================================================

```py
0001 | from pydantic import BaseModel, EmailStr , Field, ConfigDict
0002 | from datetime import datetime
0003 | 
0004 | class UserBase(BaseModel):
0005 |     username:str = Field(min_length=3, max_length=50)
0006 |     email: EmailStr  = Field(max_length=120)
0007 |     
0008 | class UserCreate(UserBase):
0009 |     password:str = Field(min_length=8, max_length=100)
0010 | 
0011 | 
0012 | class UserPublic(BaseModel):
0013 |     model_config = ConfigDict(from_attributes=True)
0014 |     username:str = Field(min_length=3, max_length=50)
0015 |     id: int
0016 | class UserPrivate(UserPublic):
0017 |     email: EmailStr  = Field(max_length=120)   
0018 |     
0019 |     
0020 | class UserUpdate(BaseModel):
0021 |     username: str | None = Field( default=None, min_length=3, max_length=50)
0022 |     email:str | None = Field( default=None, min_length=5, max_length=100)
0023 |     
0024 | class Token(BaseModel):
0025 |     access_token: str
0026 |     token_type: str
0027 |    
0028 |    
0029 | class PostBase(BaseModel):
0030 |     title:str = Field(min_length=3 , max_length=100)
0031 |     content: str = Field(min_length=10)
0032 |     
0033 | class PostCreate(PostBase):
0034 |     pass
0035 | 
0036 | class PostResponse(PostBase):
0037 |     model_config = ConfigDict(from_attributes=True)
0038 |     
0039 |     id: int
0040 |     user: UserPublic
0041 |     created_at : datetime 
0042 | 
0043 | class PostUpdate(BaseModel):
0044 |     title: str | None = Field( default=None, min_length=3, max_length=100)
0045 |     content: str | None = Field( default=None, min_length=10)
0046 |     
0047 |     

```


================================================================================
# FILE: .\auth.py
================================================================================

```py
0001 | from datetime import datetime, timedelta, UTC
0002 | import jwt
0003 | from fastapi.security import OAuth2PasswordBearer
0004 | from pwdlib import PasswordHash
0005 | from config import settings
0006 | 
0007 | ## for Authorization
0008 | from typing import Annotated
0009 | from fastapi import Depends, HTTPException, status 
0010 | from sqlalchemy import select
0011 | from sqlalchemy.orm import Session 
0012 | import models 
0013 | from database import get_db
0014 | 
0015 | 
0016 | 
0017 | password_hash = PasswordHash.recommended()
0018 | 
0019 | oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")
0020 | 
0021 | def hash_password(password: str) -> str:
0022 |     # Hash the password using pwdlib's PasswordHash
0023 |     return password_hash.hash(password)
0024 | 
0025 | def verify_password(plain_password: str, hashed_password: str) -> bool:
0026 |     # Verify the password using pwdlib's PasswordHash
0027 |     return password_hash.verify(plain_password, hashed_password)
0028 | 
0029 | def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
0030 |     to_encode = data.copy()
0031 |     if expires_delta:
0032 |         expire = datetime.now(UTC) + expires_delta
0033 |     else:
0034 |         expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
0035 |     to_encode.update({"exp": expire})
0036 |     encoded_jwt = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=settings.algorithm)
0037 |     return encoded_jwt
0038 | 
0039 | def verify_access_token(token: str) -> str | None:
0040 |     try:
0041 |         payload = jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=[settings.algorithm], options={"require": ["exp", "sub"]})
0042 |     except jwt.ExpiredSignatureError:
0043 |         return None
0044 |     except jwt.InvalidTokenError:
0045 |         return None
0046 |     else:
0047 |         return payload.get("sub")
0048 |     
0049 |     
0050 |     
0051 | # get current user def
0052 | 
0053 | def get_current_user(
0054 |     token: Annotated[str, Depends(oauth2_scheme)],
0055 |     db: Annotated[Session, Depends(get_db)],) -> models.User:
0056 |     
0057 |     user_id = verify_access_token(token)
0058 | 
0059 |     if user_id is None:
0060 |         raise HTTPException(
0061 |             status_code=status.HTTP_401_UNAUTHORIZED,
0062 |             detail="Not authenticated",
0063 |             headers={"WWW-Authenticate": "Bearer"},
0064 |         )
0065 | 
0066 |     try:
0067 |         user_id = int(user_id)
0068 |     except ValueError:
0069 |         raise HTTPException(
0070 |             status_code=status.HTTP_401_UNAUTHORIZED,
0071 |             detail="Not authenticated",
0072 |             headers={"WWW-Authenticate": "Bearer"},
0073 |         )
0074 | 
0075 |     user = db.execute(
0076 |         select(models.User).where(models.User.id == user_id)
0077 |     ).scalars().first()
0078 | 
0079 |     if user is None:
0080 |         raise HTTPException(
0081 |             status_code=status.HTTP_401_UNAUTHORIZED,
0082 |             detail="Not authenticated",
0083 |             headers={"WWW-Authenticate": "Bearer"},
0084 |         )
0085 | 
0086 |     return user
0087 | 
0088 | 
0089 | CurrentUser = Annotated[models.User, Depends(get_current_user)]

```


================================================================================
# FILE: .\config.py
================================================================================

```py
0001 | from pydantic import SecretStr
0002 | from pydantic_settings import BaseSettings, SettingsConfigDict
0003 | 
0004 | 
0005 | class Settings(BaseSettings):
0006 |     model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
0007 | 
0008 |     secret_key: SecretStr
0009 |     algorithm: str = "HS256"
0010 |     access_token_expire_minutes: int = 30
0011 |     
0012 | settings = Settings() #load settings from .env file

```


================================================================================
# FILE: .\frontend\index.html
================================================================================

```html
0001 | <!doctype html>
0002 | <html lang="en">
0003 |   <head>
0004 |     <meta charset="UTF-8" />
0005 |     <link rel="icon" type="image/svg+xml" href="/vite.svg" />
0006 |     <meta name="viewport" content="width=device-width, initial-scale=1.0" />
0007 |     <title>Fieldnotes — Technical Knowledge Base</title>
0008 |   </head>
0009 |   <body class="bg-[#fafafa] dark:bg-[#1a1a1a] transition-colors duration-200">
0010 |     <div id="root"></div>
0011 |     <script type="module" src="/src/main.tsx"></script>
0012 |   </body>
0013 | </html>

```


================================================================================
# FILE: .\frontend\postcss.config.js
================================================================================

```js
0001 | export default {
0002 |   plugins: {
0003 |     tailwindcss: {},
0004 |     autoprefixer: {},
0005 |   },
0006 | }

```


================================================================================
# FILE: .\frontend\src\App.tsx
================================================================================

```tsx
0001 | import React, { useState, useEffect } from 'react';
0002 | import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
0003 | import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
0004 | import { useAuthStore } from '@/store/authStore';
0005 | import { usePosts } from '@/hooks/usePosts';
0006 | import { useForm } from 'react-hook-form';
0007 | import { zodResolver } from '@hookform/resolvers/zod';
0008 | import * as z from 'zod';
0009 | 
0010 | import { Navbar } from '@/components/Navbar';
0011 | import { ProtectedRoute } from '@/components/ProtectedRoute';
0012 | import { Dialog } from '@/components/ui/Dialog';
0013 | import { Input } from '@/components/ui/Input';
0014 | import { Textarea } from '@/components/ui/Textarea';
0015 | import { Button } from '@/components/ui/Button';
0016 | 
0017 | import { FeedPage } from '@/pages/FeedPage';
0018 | import { PostDetailPage } from '@/pages/PostDetailPage';
0019 | import { UserProfilePage } from '@/pages/UserProfilePage';
0020 | import { UsersPage } from '@/pages/UsersPage';
0021 | import { LoginPage } from '@/pages/LoginPage';
0022 | import { RegisterPage } from '@/pages/RegisterPage';
0023 | 
0024 | import { AccountPage } from '@/pages/AccountPage';
0025 | 
0026 | const queryClient = new QueryClient({
0027 |   defaultOptions: { queries: { refetchOnWindowFocus: false, retry: 1 } },
0028 | });
0029 | 
0030 | const createPostSchema = z.object({
0031 |   title: z.string().min(3).max(100),
0032 |   content: z.string().min(10),
0033 | });
0034 | type CreatePostInput = z.infer<typeof createPostSchema>;
0035 | 
0036 | const AppContent: React.FC = () => {
0037 |   const [isWriteOpen, setIsWriteOpen] = useState(false);
0038 |   const { currentUser, isAuthenticated, isInitializing, checkAuth } = useAuthStore();
0039 |   const { useCreatePost } = usePosts();
0040 |   const createMutation = useCreatePost();
0041 | 
0042 |   // Validate the stored token (if any) once, when the app first mounts
0043 |   useEffect(() => {
0044 |     checkAuth();
0045 |   }, [checkAuth]);
0046 | 
0047 |   const { register, handleSubmit, reset, formState: { errors } } = useForm<CreatePostInput>({
0048 |     resolver: zodResolver(createPostSchema),
0049 |   });
0050 | 
0051 |   const onCreatePostSubmit = (data: CreatePostInput) => {
0052 |     if (!currentUser) return;
0053 |     createMutation.mutate(
0054 |       { title: data.title, content: data.content},
0055 |       { onSuccess: () => { setIsWriteOpen(false); reset(); } }
0056 |     );
0057 |   };
0058 | 
0059 |   // Don't render routes until we know whether the user is really authenticated
0060 |   if (isInitializing) {
0061 |     return (
0062 |       <div className="min-h-screen flex items-center justify-center bg-[#fafafa] dark:bg-[#1a1a1a]">
0063 |         <p className="text-gray-500">Loading...</p>
0064 |       </div>
0065 |     );
0066 |   }
0067 | 
0068 |   return (
0069 |     <BrowserRouter>
0070 |       <div className="min-h-screen bg-[#fafafa] dark:bg-[#1a1a1a] flex flex-col transition-colors duration-200">
0071 |         <Navbar onCreatePostClick={() => setIsWriteOpen(true)} />
0072 | 
0073 |         <main className="flex-grow max-w-4xl w-full mx-auto px-4 pt-24 pb-16">
0074 |           <Routes>
0075 |             <Route path="/login" element={isAuthenticated ? <Navigate to="/" replace /> : <LoginPage />} />
0076 |             <Route path="/signup" element={isAuthenticated ? <Navigate to="/" replace /> : <RegisterPage />} />
0077 | 
0078 |             <Route path="/" element={<ProtectedRoute><FeedPage /></ProtectedRoute>} />
0079 |             <Route path="/posts/:id" element={<ProtectedRoute><PostDetailPage /></ProtectedRoute>} />
0080 |             <Route path="/users/:id" element={<ProtectedRoute><UserProfilePage /></ProtectedRoute>} />
0081 |             <Route path="/users" element={<ProtectedRoute><UsersPage /></ProtectedRoute>} />
0082 | 
0083 |             <Route path="*" element={<Navigate to="/" replace />} />
0084 |             <Route path="/account" element={<ProtectedRoute><AccountPage /></ProtectedRoute>} />
0085 | 
0086 |           </Routes>
0087 |         </main>
0088 | 
0089 |         {isAuthenticated && (
0090 |           <Dialog isOpen={isWriteOpen} onClose={() => setIsWriteOpen(false)} title="Write a Technical Note">
0091 |             <form onSubmit={handleSubmit(onCreatePostSubmit)}>
0092 |               <div className="bg-gray-50 dark:bg-zinc-900 border border-gray-100 dark:border-zinc-800 p-3 rounded text-xs mb-4">
0093 |                 Posting as: <strong className="text-steel-500">{currentUser?.username}</strong>
0094 |               </div>
0095 |               <Input label="Log Entry Title" {...register('title')} error={errors.title?.message} />
0096 |               <Textarea label="Content" rows={8} {...register('content')} error={errors.content?.message} />
0097 |               <div className="flex items-center justify-end gap-2 mt-4 pt-4 border-t border-gray-100 dark:border-zinc-800">
0098 |                 <Button type="button" variant="ghost" onClick={() => setIsWriteOpen(false)}>Cancel</Button>
0099 |                 <Button type="submit" isLoading={createMutation.isPending}>Publish</Button>
0100 |               </div>
0101 |             </form>
0102 |           </Dialog>
0103 |         )}
0104 |       </div>
0105 |     </BrowserRouter>
0106 |   );
0107 | };
0108 | 
0109 | export default function App() {
0110 |   return (
0111 |     <QueryClientProvider client={queryClient}>
0112 |       <AppContent />
0113 |     </QueryClientProvider>
0114 |   );
0115 | }
0116 | 
0117 | 
0118 | // inside <Routes>:

```


================================================================================
# FILE: .\frontend\src\components\Navbar.tsx
================================================================================

```tsx
0001 | import React, { useEffect, useState } from 'react';
0002 | import { Link, NavLink, useNavigate } from 'react-router-dom';
0003 | import { useAuthStore } from '@/store/authStore';
0004 | import { BookOpen, Moon, Sun, PlusCircle, LogOut } from 'lucide-react';
0005 | import { Button } from './ui/Button';
0006 | 
0007 | interface NavbarProps {
0008 |   onCreatePostClick: () => void;
0009 | }
0010 | 
0011 | export const Navbar: React.FC<NavbarProps> = ({ onCreatePostClick }) => {
0012 |   const { currentUser, logout, isAuthenticated } = useAuthStore();
0013 |   const navigate = useNavigate();
0014 |   const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light');
0015 | 
0016 |   useEffect(() => {
0017 |     const root = window.document.documentElement;
0018 |     if (theme === 'dark') {
0019 |       root.classList.add('dark');
0020 |     } else {
0021 |       root.classList.remove('dark');
0022 |     }
0023 |     localStorage.setItem('theme', theme);
0024 |   }, [theme]);
0025 | 
0026 |   const handleLogout = () => {
0027 |     logout();
0028 |     navigate('/login');
0029 |   };
0030 | 
0031 |   return (
0032 |     <nav className="fixed top-0 left-0 right-0 z-40 bg-steel-500 text-white shadow-md">
0033 |       <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
0034 | 
0035 |         <Link to="/" className="flex items-center gap-2 text-xl font-bold tracking-tight text-white hover:opacity-90">
0036 |           <BookOpen className="h-6 w-6" />
0037 |           <span>Fieldnotes</span>
0038 |         </Link>
0039 | 
0040 |         <div className="flex items-center gap-5">
0041 |           {isAuthenticated && (
0042 |             <div className="flex items-center gap-4 text-sm font-medium">
0043 |               <NavLink
0044 |                 to="/"
0045 |                 className={({ isActive }) => `hover:text-steel-100 transition-colors ${isActive ? 'underline underline-offset-4 decoration-2 font-bold text-white' : 'text-steel-100'}`}
0046 |               >
0047 |                 Feed
0048 |               </NavLink>
0049 |               <NavLink
0050 |                 to="/users"
0051 |                 className={({ isActive }) => `hover:text-steel-100 transition-colors ${isActive ? 'underline underline-offset-4 decoration-2 font-bold text-white' : 'text-steel-100'}`}
0052 |               >
0053 |                 Authors
0054 |               </NavLink>
0055 |             </div>
0056 |           )}
0057 | 
0058 |           {isAuthenticated && <div className="h-6 w-[1px] bg-steel-600 hidden sm:block" />}
0059 | 
0060 |           <div className="flex items-center gap-3">
0061 |             {isAuthenticated && (
0062 |               <Button
0063 |                 onClick={onCreatePostClick}
0064 |                 className="bg-white/10 hover:bg-white/20 border border-white/20 text-white gap-2"
0065 |                 size="sm"
0066 |               >
0067 |                 <PlusCircle className="h-4 w-4" />
0068 |                 <span className="hidden sm:inline">Write Note</span>
0069 |               </Button>
0070 |             )}
0071 | 
0072 |             <button
0073 |               onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
0074 |               className="p-2 hover:bg-steel-600 rounded-full transition-colors text-white"
0075 |             >
0076 |               {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
0077 |             </button>
0078 | 
0079 |             {isAuthenticated && currentUser && (
0080 |               <>
0081 |                 {/* Links to /account — NOT /users/:id */}
0082 |                 <Link
0083 |                   to="/account"
0084 |                   className="flex items-center gap-2 hover:bg-steel-600 p-1.5 rounded-full transition-colors"
0085 |                   title="My Account Settings"
0086 |                 >
0087 |                   <div className="w-8 h-8 rounded-full bg-steel-100 text-steel-700 font-extrabold flex items-center justify-center text-sm shadow-sm">
0088 |                     {currentUser.username.substring(0, 2).toUpperCase()}
0089 |                   </div>
0090 |                 </Link>
0091 | 
0092 |                 <button
0093 |                   onClick={handleLogout}
0094 |                   className="p-2 hover:bg-steel-600 rounded-full transition-colors text-white"
0095 |                   title="Log Out"
0096 |                 >
0097 |                   <LogOut className="h-5 w-5" />
0098 |                 </button>
0099 |               </>
0100 |             )}
0101 |           </div>
0102 |         </div>
0103 |       </div>
0104 |     </nav>
0105 |   );
0106 | };

```


================================================================================
# FILE: .\frontend\src\components\ProtectedRoute.tsx
================================================================================

```tsx
0001 | import React from 'react';
0002 | import { Navigate } from 'react-router-dom';
0003 | import { useAuthStore } from '@/store/authStore';
0004 | 
0005 | export const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
0006 |   const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
0007 | 
0008 |   if (!isAuthenticated) {
0009 |     return <Navigate to="/login" replace />;
0010 |   }
0011 | 
0012 |   return <>{children}</>;
0013 | };

```


================================================================================
# FILE: .\frontend\src\components\ui\Button.tsx
================================================================================

```tsx
0001 | import React from 'react';
0002 | 
0003 | interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
0004 |   variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
0005 |   size?: 'sm' | 'md' | 'lg';
0006 |   isLoading?: boolean;
0007 | }
0008 | 
0009 | export const Button: React.FC<ButtonProps> = ({
0010 |   children,
0011 |   variant = 'primary',
0012 |   size = 'md',
0013 |   isLoading,
0014 |   className = '',
0015 |   disabled,
0016 |   ...props
0017 | }) => {
0018 |   const baseStyle = 'inline-flex items-center justify-center font-semibold rounded-md transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none';
0019 |   
0020 |   const variants = {
0021 |     primary: 'bg-steel-500 text-white hover:bg-steel-600 focus-visible:ring-steel-500',
0022 |     secondary: 'border border-gray-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-gray-700 dark:text-zinc-200 hover:bg-gray-50 dark:hover:bg-zinc-700 focus-visible:ring-steel-500',
0023 |     danger: 'bg-red-600 hover:bg-red-700 text-white focus-visible:ring-red-500',
0024 |     ghost: 'hover:bg-gray-100 dark:hover:bg-zinc-800 text-gray-700 dark:text-zinc-300'
0025 |   };
0026 | 
0027 |   const sizes = {
0028 |     sm: 'px-3 py-1.5 text-xs',
0029 |     md: 'px-4 py-2 text-sm',
0030 |     lg: 'px-5 py-2.5 text-base'
0031 |   };
0032 | 
0033 |   return (
0034 |     <button
0035 |       className={`${baseStyle} ${variants[variant]} ${sizes[size]} ${className}`}
0036 |       disabled={disabled || isLoading}
0037 |       {...props}
0038 |     >
0039 |       {isLoading ? (
0040 |         <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" fill="none" viewBox="0 0 24 24">
0041 |           <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
0042 |           <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
0043 |         </svg>
0044 |       ) : null}
0045 |       {children}
0046 |     </button>
0047 |   );
0048 | };

```


================================================================================
# FILE: .\frontend\src\components\ui\Card.tsx
================================================================================

```tsx
0001 | import React from 'react';
0002 | 
0003 | export const Card: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, className = '', ...props }) => {
0004 |   return (
0005 |     <div 
0006 |       className={`bg-white dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 rounded-lg shadow-sm hover:shadow-md transition-all duration-200 ${className}`} 
0007 |       {...props}
0008 |     >
0009 |       {children}
0010 |     </div>
0011 |   );
0012 | };

```


================================================================================
# FILE: .\frontend\src\components\ui\Dialog.tsx
================================================================================

```tsx
0001 | import React, { useEffect } from 'react';
0002 | import { X } from 'lucide-react';
0003 | 
0004 | interface DialogProps {
0005 |   isOpen: boolean;
0006 |   onClose: () => void;
0007 |   title: string;
0008 |   children: React.ReactNode;
0009 | }
0010 | 
0011 | export const Dialog: React.FC<DialogProps> = ({ isOpen, onClose, title, children }) => {
0012 |   useEffect(() => {
0013 |     const handleEscape = (e: KeyboardEvent) => {
0014 |       if (e.key === 'Escape') onClose();
0015 |     };
0016 |     if (isOpen) {
0017 |       document.body.style.overflow = 'hidden';
0018 |       window.addEventListener('keydown', handleEscape);
0019 |     }
0020 |     return () => {
0021 |       document.body.style.overflow = '';
0022 |       window.removeEventListener('keydown', handleEscape);
0023 |     };
0024 |   }, [isOpen, onClose]);
0025 | 
0026 |   if (!isOpen) return null;
0027 | 
0028 |   return (
0029 |     <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
0030 |       <div 
0031 |         className="fixed inset-0 bg-black/60 backdrop-blur-sm transition-opacity" 
0032 |         onClick={onClose} 
0033 |       />
0034 |       
0035 |       <div className="relative w-full max-w-lg bg-white dark:bg-zinc-950 border border-gray-250 dark:border-zinc-800 rounded-lg shadow-xl overflow-hidden z-10 animate-in fade-in zoom-in-95 duration-250">
0036 |         <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-zinc-800 bg-gray-50 dark:bg-zinc-900/50">
0037 |           <h3 className="text-lg font-semibold text-gray-900 dark:text-zinc-100">{title}</h3>
0038 |           <button 
0039 |             onClick={onClose} 
0040 |             className="text-gray-400 hover:text-gray-500 dark:hover:text-zinc-300 rounded-full p-1 transition-colors"
0041 |           >
0042 |             <X className="h-5 w-5" />
0043 |           </button>
0044 |         </div>
0045 |         <div className="p-6 overflow-y-auto max-h-[80vh]">
0046 |           {children}
0047 |         </div>
0048 |       </div>
0049 |     </div>
0050 |   );
0051 | };

```


================================================================================
# FILE: .\frontend\src\components\ui\Input.tsx
================================================================================

```tsx
0001 | import React, { forwardRef } from 'react';
0002 | 
0003 | interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
0004 |   label?: string;
0005 |   error?: string;
0006 | }
0007 | 
0008 | export const Input = forwardRef<HTMLInputElement, InputProps>(
0009 |   ({ label, error, className = '', ...props }, ref) => {
0010 |     return (
0011 |       <div className="w-full mb-4">
0012 |         {label && (
0013 |           <label className="block text-sm font-medium text-gray-700 dark:text-zinc-300 mb-1">
0014 |             {label}
0015 |           </label>
0016 |         )}
0017 |         <input
0018 |           ref={ref}
0019 |           className={`w-full px-3 py-2 bg-white dark:bg-zinc-850 border ${
0020 |             error ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 dark:border-zinc-700 focus:ring-steel-500'
0021 |           } rounded-md text-sm text-gray-900 dark:text-zinc-100 placeholder-gray-400 focus:outline-none focus:ring-2 transition-colors ${className}`}
0022 |           {...props}
0023 |         />
0024 |         {error && <p className="mt-1 text-xs text-red-500 font-medium">{error}</p>}
0025 |       </div>
0026 |     );
0027 |   }
0028 | );
0029 | 
0030 | Input.displayName = 'Input';

```


================================================================================
# FILE: .\frontend\src\components\ui\Textarea.tsx
================================================================================

```tsx
0001 | import React, { forwardRef } from 'react';
0002 | 
0003 | interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
0004 |   label?: string;
0005 |   error?: string;
0006 | }
0007 | 
0008 | export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
0009 |   ({ label, error, className = '', ...props }, ref) => {
0010 |     return (
0011 |       <div className="w-full mb-4">
0012 |         {label && (
0013 |           <label className="block text-sm font-medium text-gray-700 dark:text-zinc-300 mb-1">
0014 |             {label}
0015 |           </label>
0016 |         )}
0017 |         <textarea
0018 |           ref={ref}
0019 |           className={`w-full px-3 py-2 bg-white dark:bg-zinc-850 border ${
0020 |             error ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 dark:border-zinc-700 focus:ring-steel-500'
0021 |           } rounded-md text-sm text-gray-900 dark:text-zinc-100 placeholder-gray-400 focus:outline-none focus:ring-2 transition-colors ${className}`}
0022 |           {...props}
0023 |         />
0024 |         {error && <p className="mt-1 text-xs text-red-500 font-medium">{error}</p>}
0025 |       </div>
0026 |     );
0027 |   }
0028 | );
0029 | 
0030 | Textarea.displayName = 'Textarea';

```


================================================================================
# FILE: .\frontend\src\hooks\usePosts.ts
================================================================================

```ts
0001 | import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
0002 | import { api } from '@/lib/api';
0003 | import { Post, PostCreate, PostUpdate } from '@/types/api';
0004 | 
0005 | export const usePosts = () => {
0006 |   const queryClient = useQueryClient();
0007 | 
0008 |   const useGetPosts = () => useQuery<Post[]>({
0009 |     queryKey: ['posts'],
0010 |     queryFn: async () => {
0011 |       const { data } = await api.get<Post[]>('/posts');
0012 |       return data;
0013 |     },
0014 |   });
0015 | 
0016 |   const useGetPost = (id: number) => useQuery<Post>({
0017 |     queryKey: ['posts', id],
0018 |     queryFn: async () => {
0019 |       const { data } = await api.get<Post>(`/posts/${id}`);
0020 |       return data;
0021 |     },
0022 |     enabled: !isNaN(id) && id > 0,
0023 |   });
0024 | 
0025 |   const useCreatePost = () => useMutation({
0026 |     mutationFn: async (payload: PostCreate) => {
0027 |       const { data } = await api.post<Post>('/posts', payload);
0028 |       return data;
0029 |     },
0030 |     onSuccess: () => {
0031 |       queryClient.invalidateQueries({ queryKey: ['posts'] });
0032 |     },
0033 |   });
0034 | 
0035 |   const useUpdatePost = (id: number) => useMutation({
0036 |     mutationFn: async (payload: PostUpdate) => {
0037 |       const { data } = await api.patch<Post>(`/posts/${id}`, payload);
0038 |       return data;
0039 |     },
0040 |     onSuccess: () => {
0041 |       queryClient.invalidateQueries({ queryKey: ['posts'] });
0042 |       queryClient.invalidateQueries({ queryKey: ['posts', id] });
0043 |     },
0044 |   });
0045 | 
0046 |   const useDeletePost = () => useMutation({
0047 |     mutationFn: async (id: number) => {
0048 |       await api.delete(`/posts/${id}`);
0049 |     },
0050 |     onSuccess: () => {
0051 |       queryClient.invalidateQueries({ queryKey: ['posts'] });
0052 |     },
0053 |   });
0054 | 
0055 |   return {
0056 |     useGetPosts,
0057 |     useGetPost,
0058 |     useCreatePost,
0059 |     useUpdatePost,
0060 |     useDeletePost,
0061 |   };
0062 | };

```


================================================================================
# FILE: .\frontend\src\hooks\useUsers.ts
================================================================================

```ts
0001 | import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
0002 | import { api } from '@/lib/api';
0003 | import { User, UserUpdate } from '@/types/api';
0004 | import { useAuthStore } from '@/store/authStore';
0005 | 
0006 | export const useUsers = () => {
0007 |   const queryClient = useQueryClient();
0008 |   const updateProfileState = useAuthStore((state) => state.updateProfileState);
0009 | 
0010 |   const useGetUsers = () => useQuery<User[]>({
0011 |     queryKey: ['users'],
0012 |     queryFn: async () => {
0013 |       const { data } = await api.get<User[]>('/users');
0014 |       return data;
0015 |     },
0016 |   });
0017 | 
0018 |   const useGetUser = (id: number) => useQuery<User>({
0019 |     queryKey: ['users', id],
0020 |     queryFn: async () => {
0021 |       const { data } = await api.get<User>(`/users/${id}`);
0022 |       return data;
0023 |     },
0024 |     enabled: !isNaN(id) && id > 0,
0025 |   });
0026 | 
0027 |   const useUpdateUser = (id: number) => useMutation({
0028 |     mutationFn: async (payload: UserUpdate) => {
0029 |       const { data } = await api.patch<User>(`/users/${id}`, payload);
0030 |       return data;
0031 |     },
0032 |     onSuccess: (data) => {
0033 |       queryClient.invalidateQueries({ queryKey: ['users'] });
0034 |       queryClient.invalidateQueries({ queryKey: ['users', id] });
0035 |       queryClient.invalidateQueries({ queryKey: ['posts'] });
0036 |       // Sync update with active auth store state if editing oneself
0037 |       updateProfileState(data);
0038 |     },
0039 |   });
0040 | 
0041 |   const useDeleteUser = () => useMutation({
0042 |     mutationFn: async (id: number) => {
0043 |       await api.delete(`/users/${id}`);
0044 |     },
0045 |     onSuccess: () => {
0046 |       queryClient.invalidateQueries({ queryKey: ['users'] });
0047 |       queryClient.invalidateQueries({ queryKey: ['posts'] });
0048 |     },
0049 |   });
0050 | 
0051 |   return {
0052 |     useGetUsers,
0053 |     useGetUser,
0054 |     useUpdateUser,
0055 |     useDeleteUser,
0056 |   };
0057 | };

```


================================================================================
# FILE: .\frontend\src\index.css
================================================================================

```css
0001 | @tailwind base;
0002 | @tailwind components;
0003 | @tailwind utilities;
0004 | 
0005 | @layer base {
0006 |   body {
0007 |     @apply font-body text-[#333333] dark:text-[#e0e0e0] antialiased;
0008 |   }
0009 |   
0010 |   h1, h2, h3, h4, h5, h6 {
0011 |     @apply font-heading text-[#444444] dark:text-[#f0f0f0] font-semibold;
0012 |   }
0013 | }
0014 | 
0015 | /* Scrollbar customizations for polished UI feel */
0016 | ::-webkit-scrollbar {
0017 |   width: 8px;
0018 | }
0019 | ::-webkit-scrollbar-track {
0020 |   @apply bg-transparent;
0021 | }
0022 | ::-webkit-scrollbar-thumb {
0023 |   @apply bg-gray-300 dark:bg-zinc-700 rounded-full hover:bg-gray-400 dark:hover:bg-zinc-600;
0024 | }

```


================================================================================
# FILE: .\frontend\src\lib\api.ts
================================================================================

```ts
0001 | import axios from 'axios';
0002 | import { useAuthStore } from '@/store/authStore';
0003 | 
0004 | export const api = axios.create({
0005 |   baseURL: 'http://localhost:8000/api',
0006 | });
0007 | 
0008 | // Attach the JWT to every outgoing request automatically
0009 | api.interceptors.request.use((config) => {
0010 |   const token = useAuthStore.getState().token;
0011 |   if (token) {
0012 |     config.headers.Authorization = `Bearer ${token}`;
0013 |   }
0014 |   return config;
0015 | });
0016 | 
0017 | // If any request comes back 401 (expired/invalid token), force logout
0018 | api.interceptors.response.use(
0019 |   (response) => response,
0020 |   (error) => {
0021 |     if (error.response?.status === 401) {
0022 |       useAuthStore.getState().logout();
0023 |     }
0024 |     const errorData = error.response?.data;
0025 |     return Promise.reject(errorData || { error: { message: 'Network connection error' } });
0026 |   }
0027 | );

```


================================================================================
# FILE: .\frontend\src\main.tsx
================================================================================

```tsx
0001 | import React from 'react'
0002 | import ReactDOM from 'react-dom/client'
0003 | import App from './App'
0004 | import './index.css'
0005 | 
0006 | ReactDOM.createRoot(document.getElementById('root')!).render(
0007 |   <React.StrictMode>
0008 |     <App />
0009 |   </React.StrictMode>,
0010 | )

```


================================================================================
# FILE: .\frontend\src\pages\AccountPage.tsx
================================================================================

```tsx
0001 | import React, { useState } from 'react';
0002 | import { useNavigate } from 'react-router-dom';
0003 | import { useAuthStore } from '@/store/authStore';
0004 | import { useUsers } from '@/hooks/useUsers';
0005 | import { usePosts } from '@/hooks/usePosts';
0006 | import { Card } from '@/components/ui/Card';
0007 | import { Button } from '@/components/ui/Button';
0008 | import { Dialog } from '@/components/ui/Dialog';
0009 | import { Input } from '@/components/ui/Input';
0010 | import { useForm } from 'react-hook-form';
0011 | import { zodResolver } from '@hookform/resolvers/zod';
0012 | import * as z from 'zod';
0013 | import { Link } from 'react-router-dom';
0014 | import { User, Settings, Trash, Terminal, Calendar, Mail, Edit } from 'lucide-react';
0015 | 
0016 | const profileUpdateSchema = z.object({
0017 |   username: z.string().min(3, 'Username must be at least 3').max(50),
0018 |   email: z.string().email('Please enter a valid email'),
0019 | });
0020 | 
0021 | type ProfileFormInput = z.infer<typeof profileUpdateSchema>;
0022 | 
0023 | export const AccountPage: React.FC = () => {
0024 |   const navigate = useNavigate();
0025 |   const { currentUser, logout, checkAuth } = useAuthStore();
0026 |   const { useUpdateUser, useDeleteUser } = useUsers();
0027 |   const { useGetPosts } = usePosts();
0028 | 
0029 |   const { data: posts } = useGetPosts();
0030 |   const [isSettingsOpen, setIsSettingsOpen] = useState(false);
0031 | 
0032 |   // Only runs if currentUser exists (guaranteed by ProtectedRoute)
0033 |   const updateMutation = useUpdateUser(currentUser!.id);
0034 |   const deleteMutation = useDeleteUser();
0035 | 
0036 |   // Form always seeded from currentUser (UserPrivate — has email)
0037 |   const { register, handleSubmit, formState: { errors } } = useForm<ProfileFormInput>({
0038 |     resolver: zodResolver(profileUpdateSchema),
0039 |     values: {
0040 |       username: currentUser!.username,
0041 |       email: currentUser!.email,
0042 |     },
0043 |   });
0044 | 
0045 |   // My posts only — filtered client-side from the full posts list
0046 |   const myPosts = posts?.filter((p) => p.user?.id === currentUser!.id) || [];
0047 | 
0048 |   const onProfileUpdate = (data: ProfileFormInput) => {
0049 |     updateMutation.mutate(data, {
0050 |       onSuccess: async () => {
0051 |         await checkAuth(); // re-fetch /me so authStore.currentUser reflects new username/email immediately
0052 |         setIsSettingsOpen(false);
0053 |       },
0054 |     });
0055 |   };
0056 | 
0057 |   const onProfileDelete = () => {
0058 |     if (window.confirm('WARNING: This permanently deletes your account and all your posts.')) {
0059 |       deleteMutation.mutate(currentUser!.id, {
0060 |         onSuccess: () => {
0061 |           logout();
0062 |           navigate('/signup');
0063 |         },
0064 |       });
0065 |     }
0066 |   };
0067 | 
0068 |   if (!currentUser) return null; // ProtectedRoute handles this, just a safety guard
0069 | 
0070 |   return (
0071 |     <div className="space-y-6">
0072 | 
0073 |       {/* Profile Header Card */}
0074 |       <Card className="p-6">
0075 |         <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
0076 |           <div className="flex flex-col sm:flex-row items-center gap-4 text-center sm:text-left">
0077 |             <div className="w-16 h-16 rounded-full bg-steel-500 text-white font-extrabold flex items-center justify-center text-2xl shadow-md border-2 border-white dark:border-zinc-800">
0078 |               {currentUser.username.substring(0, 2).toUpperCase()}
0079 |             </div>
0080 |             <div>
0081 |               <h1 className="text-2xl font-bold flex items-center justify-center sm:justify-start gap-1">
0082 |                 <User className="h-5 w-5 text-steel-500" />
0083 |                 <span>{currentUser.username}</span>
0084 |               </h1>
0085 |               {/* Email shows correctly because currentUser comes from /me (UserPrivate) */}
0086 |               <p className="text-xs text-gray-500 dark:text-zinc-400 flex items-center gap-1 mt-1">
0087 |                 <Mail className="h-3 w-3" />
0088 |                 <span>{currentUser.email}</span>
0089 |               </p>
0090 |               <p className="text-xs font-semibold text-steel-500 mt-2 bg-steel-100 dark:bg-zinc-800/80 px-2 py-0.5 rounded-full inline-block">
0091 |                 {myPosts.length} {myPosts.length === 1 ? 'Note' : 'Notes'} Published
0092 |               </p>
0093 |             </div>
0094 |           </div>
0095 | 
0096 |           <Button
0097 |             variant="secondary"
0098 |             size="sm"
0099 |             onClick={() => setIsSettingsOpen(true)}
0100 |             className="gap-1.5 self-center sm:self-start"
0101 |           >
0102 |             <Settings className="h-4 w-4" />
0103 |             <span>Edit Profile</span>
0104 |           </Button>
0105 |         </div>
0106 |       </Card>
0107 | 
0108 |       {/* My Posts */}
0109 |       <div className="space-y-4">
0110 |         <h2 className="text-lg font-bold border-b border-gray-100 dark:border-zinc-800 pb-2">
0111 |           My Notes
0112 |         </h2>
0113 | 
0114 |         {myPosts.length === 0 ? (
0115 |           <Card className="p-8 text-center text-gray-500">
0116 |             You haven't written any notes yet.
0117 |           </Card>
0118 |         ) : (
0119 |           myPosts.map((post) => (
0120 |             <Card key={post.id} className="p-6">
0121 |               <div className="flex items-center gap-1.5 text-xs text-gray-500 dark:text-zinc-400 mb-2">
0122 |                 <Calendar className="h-3 w-3" />
0123 |                 <span>{new Date(post.created_at).toLocaleDateString()}</span>
0124 |               </div>
0125 |               <h3 className="text-lg font-bold mb-2">
0126 |                 <Link
0127 |                   to={`/posts/${post.id}`}
0128 |                   className="text-gray-900 dark:text-zinc-100 hover:text-steel-500"
0129 |                 >
0130 |                   {post.title}
0131 |                 </Link>
0132 |               </h3>
0133 |               <p className="text-gray-600 dark:text-zinc-300 text-sm line-clamp-3 leading-relaxed whitespace-pre-wrap">
0134 |                 {post.content}
0135 |               </p>
0136 |               <div className="mt-3 flex items-center gap-3">
0137 |                 <Link
0138 |                   to={`/posts/${post.id}`}
0139 |                   className="inline-flex items-center gap-1 text-xs font-bold text-steel-500 hover:underline"
0140 |                 >
0141 |                   <Terminal className="h-3.5 w-3.5" />
0142 |                   <span>Open</span>
0143 |                 </Link>
0144 |                 <Link
0145 |                   to={`/posts/${post.id}`}
0146 |                   className="inline-flex items-center gap-1 text-xs font-bold text-gray-400 hover:text-steel-500 hover:underline"
0147 |                 >
0148 |                   <Edit className="h-3.5 w-3.5" />
0149 |                   <span>Edit</span>
0150 |                 </Link>
0151 |               </div>
0152 |             </Card>
0153 |           ))
0154 |         )}
0155 |       </div>
0156 | 
0157 |       {/* Account Settings Dialog */}
0158 |       <Dialog
0159 |         isOpen={isSettingsOpen}
0160 |         onClose={() => setIsSettingsOpen(false)}
0161 |         title="Account Settings"
0162 |       >
0163 |         <form onSubmit={handleSubmit(onProfileUpdate)}>
0164 |           <Input
0165 |             label="Username"
0166 |             {...register('username')}
0167 |             error={errors.username?.message}
0168 |           />
0169 |           <Input
0170 |             label="Email address"
0171 |             type="email"
0172 |             {...register('email')}
0173 |             error={errors.email?.message}
0174 |           />
0175 | 
0176 |           <div className="flex items-center justify-between mt-6 pt-4 border-t border-gray-100 dark:border-zinc-800">
0177 |             <Button
0178 |               type="button"
0179 |               variant="danger"
0180 |               className="gap-1"
0181 |               onClick={onProfileDelete}
0182 |               isLoading={deleteMutation.isPending}
0183 |             >
0184 |               <Trash className="h-4 w-4" />
0185 |               <span>Delete Account</span>
0186 |             </Button>
0187 | 
0188 |             <div className="flex gap-2">
0189 |               <Button type="button" variant="ghost" onClick={() => setIsSettingsOpen(false)}>
0190 |                 Cancel
0191 |               </Button>
0192 |               <Button type="submit" isLoading={updateMutation.isPending}>
0193 |                 Save Changes
0194 |               </Button>
0195 |             </div>
0196 |           </div>
0197 |         </form>
0198 |       </Dialog>
0199 |     </div>
0200 |   );
0201 | };

```


================================================================================
# FILE: .\frontend\src\pages\FeedPage.tsx
================================================================================

```tsx
0001 | import React from 'react';
0002 | import { Link } from 'react-router-dom';
0003 | import { usePosts } from '@/hooks/usePosts';
0004 | import { Card } from '@/components/ui/Card';
0005 | import { AlertCircle, Calendar, MessageSquare, Terminal } from 'lucide-react';
0006 | 
0007 | export const FeedPage: React.FC = () => {
0008 |   const { useGetPosts } = usePosts();
0009 |   const { data: posts, isLoading, error } = useGetPosts();
0010 | 
0011 |   if (isLoading) {
0012 |     return (
0013 |       <div className="space-y-4">
0014 |         {[1, 2, 3].map((n) => (
0015 |           <div key={n} className="animate-pulse bg-white dark:bg-zinc-900 border border-gray-255 dark:border-zinc-800 p-6 rounded-lg">
0016 |             <div className="flex items-center gap-4 mb-4">
0017 |               <div className="w-12 h-12 bg-gray-200 dark:bg-zinc-800 rounded-full" />
0018 |               <div className="flex-1 space-y-2">
0019 |                 <div className="h-4 bg-gray-200 dark:bg-zinc-800 rounded w-1/4" />
0020 |                 <div className="h-3 bg-gray-200 dark:bg-zinc-800 rounded w-1/6" />
0021 |               </div>
0022 |             </div>
0023 |             <div className="h-6 bg-gray-200 dark:bg-zinc-800 rounded w-3/4 mb-3" />
0024 |             <div className="h-4 bg-gray-200 dark:bg-zinc-800 rounded w-full" />
0025 |           </div>
0026 |         ))}
0027 |       </div>
0028 |     );
0029 |   }
0030 | 
0031 |   if (error) {
0032 |     return (
0033 |       <div className="flex flex-col items-center justify-center p-8 text-center bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/30 rounded-lg">
0034 |         <AlertCircle className="h-12 w-12 text-red-500 mb-2" />
0035 |         <h3 className="text-lg font-semibold text-red-800 dark:text-red-200">Error Connecting to Backend</h3>
0036 |         <p className="text-sm text-red-600 dark:text-red-400 mt-1">Make sure uvicorn is running on port 8000.</p>
0037 |       </div>
0038 |     );
0039 |   }
0040 | 
0041 |   return (
0042 |     <div className="space-y-6">
0043 |       <div className="border-b border-gray-200 dark:border-zinc-850 pb-4">
0044 |         <h1 className="text-3xl font-extrabold flex items-center gap-2">
0045 |           <Terminal className="h-8 w-8 text-steel-500" />
0046 |           <span>Latest Notes</span>
0047 |         </h1>
0048 |         <p className="text-gray-500 dark:text-zinc-400 mt-1 text-sm">A collaborative technical diary of design logs, commands, and notes.</p>
0049 |       </div>
0050 | 
0051 |       {posts && posts.length === 0 ? (
0052 |         <Card className="p-8 text-center">
0053 |           <MessageSquare className="h-12 w-12 text-gray-300 mx-auto mb-2" />
0054 |           <p className="text-gray-500 dark:text-zinc-400">No logs posted yet. Be the first to share your field notes!</p>
0055 |         </Card>
0056 |       ) : (
0057 |         <div className="space-y-4">
0058 |           {posts?.map((post) => (
0059 |             <Card key={post.id} className="p-6">
0060 |               <article className="flex flex-col sm:flex-row items-start gap-4">
0061 |                 
0062 |                 <Link to={`/users/${post.user?.id}`} className="flex-shrink-0">
0063 |                   <div className="w-12 h-12 rounded-full bg-steel-100 dark:bg-zinc-800 text-steel-700 dark:text-steel-300 font-extrabold flex items-center justify-center text-sm shadow-inner border border-gray-100 dark:border-zinc-750 hover:border-steel-500 transition-colors">
0064 |                     {post.user?.username?.substring(0, 2).toUpperCase() || "UN"}
0065 |                   </div>
0066 |                 </Link>
0067 | 
0068 |                 <div className="flex-grow">
0069 |                   <div className="flex flex-wrap items-center gap-2 text-xs text-gray-500 dark:text-zinc-400 mb-2 border-b border-gray-100 dark:border-zinc-800/80 pb-2">
0070 |                     <Link to={`/users/${post.user?.id}`} className="font-bold text-steel-500 hover:underline">
0071 |                       {post.user?.username || "Anonymous"}
0072 |                     </Link>
0073 |                     <span>•</span>
0074 |                     <span className="flex items-center gap-1">
0075 |                       <Calendar className="h-3 w-3" />
0076 |                       {new Date(post.created_at).toLocaleDateString(undefined, {
0077 |                         month: 'short',
0078 |                         day: 'numeric',
0079 |                         year: 'numeric'
0080 |                       })}
0081 |                     </span>
0082 |                   </div>
0083 | 
0084 |                   <h2 className="text-xl font-bold mb-2">
0085 |                     <Link to={`/posts/${post.id}`} className="text-gray-900 dark:text-zinc-100 hover:text-steel-500 transition-colors">
0086 |                       {post.title}
0087 |                     </Link>
0088 |                   </h2>
0089 | 
0090 |                   <p className="text-gray-600 dark:text-zinc-300 line-clamp-3 text-sm leading-relaxed whitespace-pre-wrap">
0091 |                     {post.content}
0092 |                   </p>
0093 | 
0094 |                   <div className="mt-4">
0095 |                     <Link to={`/posts/${post.id}`} className="text-xs font-bold text-steel-500 hover:text-steel-600">
0096 |                       Read full entry →
0097 |                     </Link>
0098 |                   </div>
0099 |                 </div>
0100 | 
0101 |               </article>
0102 |             </Card>
0103 |           ))}
0104 |         </div>
0105 |       )}
0106 |     </div>
0107 |   );
0108 | };

```


================================================================================
# FILE: .\frontend\src\pages\LoginPage.tsx
================================================================================

```tsx
0001 | import React, { useState } from 'react';
0002 | import { Link, useNavigate } from 'react-router-dom';
0003 | import { useAuthStore } from '@/store/authStore';
0004 | import { Card } from '@/components/ui/Card';
0005 | import { Input } from '@/components/ui/Input';
0006 | import { Button } from '@/components/ui/Button';
0007 | import { useForm } from 'react-hook-form';
0008 | import { zodResolver } from '@hookform/resolvers/zod';
0009 | import * as z from 'zod';
0010 | import { BookOpen, Key, AlertTriangle } from 'lucide-react';
0011 | 
0012 | const loginSchema = z.object({
0013 |   email: z.string().email('Please enter a valid email address'),
0014 |   password: z.string().min(1, 'Please enter your password'),
0015 | });
0016 | 
0017 | type LoginFormInput = z.infer<typeof loginSchema>;
0018 | 
0019 | export const LoginPage: React.FC = () => {
0020 |   const login = useAuthStore((state) => state.login);
0021 |   const navigate = useNavigate();
0022 |   const [apiError, setApiError] = useState<string | null>(null);
0023 |   const [loading, setLoading] = useState(false);
0024 | 
0025 |   const { register, handleSubmit, formState: { errors } } = useForm<LoginFormInput>({
0026 |     resolver: zodResolver(loginSchema),
0027 |   });
0028 | 
0029 |   const onSubmit = async (data: LoginFormInput) => {
0030 |     setLoading(true);
0031 |     setApiError(null);
0032 |     try {
0033 |       await login(data.email, data.password);
0034 |       navigate('/');
0035 |     } catch (err: any) {
0036 |       setApiError(err?.error?.message || 'Incorrect email or password');
0037 |     } finally {
0038 |       setLoading(false);
0039 |     }
0040 |   };
0041 | 
0042 |   return (
0043 |     <div className="max-w-md mx-auto mt-12">
0044 |       <div className="text-center mb-8">
0045 |         <BookOpen className="h-12 w-12 text-steel-500 mx-auto mb-3" />
0046 |         <h1 className="text-3xl font-extrabold tracking-tight">Log into Fieldnotes</h1>
0047 |         <p className="text-sm text-gray-500 mt-1">Sign in with your registered email and password</p>
0048 |       </div>
0049 | 
0050 |       <Card className="p-6">
0051 |         {apiError && (
0052 |           <div className="flex items-center gap-2 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/40 p-3 rounded-md mb-4 text-sm text-red-600 dark:text-red-400">
0053 |             <AlertTriangle className="h-4.5 w-4.5 flex-shrink-0" />
0054 |             <span>{apiError}</span>
0055 |           </div>
0056 |         )}
0057 | 
0058 |         <form onSubmit={handleSubmit(onSubmit)}>
0059 |           <Input
0060 |             label="Email"
0061 |             type="email"
0062 |             placeholder="you@example.com"
0063 |             {...register('email')}
0064 |             error={errors.email?.message}
0065 |           />
0066 |           <Input
0067 |             label="Password"
0068 |             type="password"
0069 |             placeholder="••••••••"
0070 |             {...register('password')}
0071 |             error={errors.password?.message}
0072 |           />
0073 | 
0074 |           <Button type="submit" className="w-full justify-center gap-1.5 mt-2" isLoading={loading}>
0075 |             <Key className="h-4 w-4" />
0076 |             <span>Sign In</span>
0077 |           </Button>
0078 |         </form>
0079 |       </Card>
0080 | 
0081 |       <div className="text-center mt-6 text-sm text-gray-500">
0082 |         New author?{' '}
0083 |         <Link to="/signup" className="text-steel-500 hover:underline font-bold">
0084 |           Register new account
0085 |         </Link>
0086 |       </div>
0087 |     </div>
0088 |   );
0089 | };

```


================================================================================
# FILE: .\frontend\src\pages\PostDetailPage.tsx
================================================================================

```tsx
0001 | import React, { useState } from 'react';
0002 | import { useParams, useNavigate, Link } from 'react-router-dom';
0003 | import { usePosts } from '@/hooks/usePosts';
0004 | import { useAuthStore } from '@/store/authStore';
0005 | import { Card } from '@/components/ui/Card';
0006 | import { Button } from '@/components/ui/Button';
0007 | import { Dialog } from '@/components/ui/Dialog';
0008 | import { Input } from '@/components/ui/Input';
0009 | import { Textarea } from '@/components/ui/Textarea';
0010 | import { useForm } from 'react-hook-form';
0011 | import { zodResolver } from '@hookform/resolvers/zod';
0012 | import * as z from 'zod';
0013 | import { Calendar, Trash2, Edit, ArrowLeft, Terminal } from 'lucide-react';
0014 | 
0015 | const updateSchema = z.object({
0016 |   title: z.string().min(3, "Title must be at least 3 characters").max(100),
0017 |   content: z.string().min(10, "Content must contain at least 10 characters"),
0018 | });
0019 | 
0020 | type UpdateFormInput = z.infer<typeof updateSchema>;
0021 | 
0022 | export const PostDetailPage: React.FC = () => {
0023 |   const { id } = useParams<{ id: string }>();
0024 |   const navigate = useNavigate();
0025 |   const postId = Number(id);
0026 | 
0027 |   const { currentUser } = useAuthStore();
0028 |   const { useGetPost, useUpdatePost, useDeletePost } = usePosts();
0029 |   
0030 |   const { data: post, isLoading, error } = useGetPost(postId);
0031 |   const updateMutation = useUpdatePost(postId);
0032 |   const deleteMutation = useDeletePost();
0033 | 
0034 |   const [isEditOpen, setIsEditOpen] = useState(false);
0035 | 
0036 |   const { register, handleSubmit, formState: { errors } } = useForm<UpdateFormInput>({
0037 |     resolver: zodResolver(updateSchema),
0038 |     values: post ? { title: post.title, content: post.content } : undefined,
0039 |   });
0040 | 
0041 |   const onUpdateSubmit = (data: UpdateFormInput) => {
0042 |     updateMutation.mutate(data, {
0043 |       onSuccess: () => {
0044 |         setIsEditOpen(false);
0045 |       }
0046 |     });
0047 |   };
0048 | 
0049 |   const onDelete = () => {
0050 |     if (window.confirm("Are you sure you want to delete this log entry?")) {
0051 |       deleteMutation.mutate(postId, {
0052 |         onSuccess: () => navigate('/')
0053 |       });
0054 |     }
0055 |   };
0056 | 
0057 |   if (isLoading) return <div className="animate-pulse bg-white p-6 rounded-lg h-64" />;
0058 |   if (error || !post) return <div className="text-center p-8">Log entry not found.</div>;
0059 | 
0060 |   // Use the nested user.id relationship to check ownership
0061 |   const isAuthor = currentUser?.id === post.user?.id;
0062 | 
0063 |   return (
0064 |     <div className="space-y-4">
0065 |       <button onClick={() => navigate(-1)} className="inline-flex items-center gap-1.5 text-xs font-bold text-gray-500 hover:text-steel-500 transition-colors">
0066 |         <ArrowLeft className="h-4 w-4" />
0067 |         <span>Back to feed</span>
0068 |       </button>
0069 | 
0070 |       <Card className="p-6">
0071 |         <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-gray-100 dark:border-zinc-800 pb-4 mb-4">
0072 |           <div className="flex items-center gap-4">
0073 |             <Link to={`/users/${post.user?.id}`}>
0074 |               <div className="w-12 h-12 rounded-full bg-steel-100 dark:bg-zinc-800 text-steel-700 dark:text-steel-300 font-extrabold flex items-center justify-center text-sm shadow-inner border border-gray-100">
0075 |                 {post.user?.username.substring(0, 2).toUpperCase()}
0076 |               </div>
0077 |             </Link>
0078 |             <div>
0079 |               <div>
0080 |                 <Link to={`/users/${post.user?.id}`} className="font-bold text-steel-500 hover:underline">
0081 |                   {post.user?.username}
0082 |                 </Link>
0083 |               </div>
0084 |               <p className="text-xs text-gray-500 flex items-center gap-1 mt-0.5">
0085 |                 <Calendar className="h-3 w-3" />
0086 |                 {new Date(post.created_at).toLocaleDateString(undefined, {
0087 |                   weekday: 'long',
0088 |                   year: 'numeric',
0089 |                   month: 'long',
0090 |                   day: 'numeric'
0091 |                 })}
0092 |               </p>
0093 |             </div>
0094 |           </div>
0095 | 
0096 |           {isAuthor && (
0097 |             <div className="flex items-center gap-2 self-end md:self-auto">
0098 |               <Button size="sm" variant="secondary" onClick={() => setIsEditOpen(true)} className="gap-1">
0099 |                 <Edit className="h-3.5 w-3.5" />
0100 |                 <span>Edit</span>
0101 |               </Button>
0102 |               <Button size="sm" variant="danger" onClick={onDelete} className="gap-1" isLoading={deleteMutation.isPending}>
0103 |                 <Trash2 className="h-3.5 w-3.5" />
0104 |                 <span>Delete</span>
0105 |               </Button>
0106 |             </div>
0107 |           )}
0108 |         </div>
0109 | 
0110 |         <h1 className="text-2xl md:text-3xl font-extrabold text-gray-900 dark:text-zinc-100 mb-6 flex items-start gap-2">
0111 |           <Terminal className="h-7 w-7 text-steel-500 mt-1 flex-shrink-0" />
0112 |           <span>{post.title}</span>
0113 |         </h1>
0114 | 
0115 |         <div className="text-gray-700 dark:text-zinc-200 text-sm leading-relaxed whitespace-pre-wrap font-sans bg-gray-50/50 dark:bg-zinc-950/20 p-4 border border-gray-100 dark:border-zinc-800/80 rounded-md">
0116 |           {post.content}
0117 |         </div>
0118 |       </Card>
0119 | 
0120 |       <Dialog isOpen={isEditOpen} onClose={() => setIsEditOpen(false)} title="Edit Note Details">
0121 |         <form onSubmit={handleSubmit(onUpdateSubmit)}>
0122 |           <Input label="Title" {...register('title')} error={errors.title?.message} />
0123 |           <Textarea label="Content / Console payload" rows={8} {...register('content')} error={errors.content?.message} />
0124 |           <div className="flex items-center justify-end gap-2 mt-4 pt-4 border-t border-gray-100 dark:border-zinc-800">
0125 |             <Button type="button" variant="ghost" onClick={() => setIsEditOpen(false)}>Cancel</Button>
0126 |             <Button type="submit" isLoading={updateMutation.isPending}>Save Changes</Button>
0127 |           </div>
0128 |         </form>
0129 |       </Dialog>
0130 |     </div>
0131 |   );
0132 | };

```


================================================================================
# FILE: .\frontend\src\pages\RegisterPage.tsx
================================================================================

```tsx
0001 | import React, { useState } from 'react';
0002 | import { Link, useNavigate } from 'react-router-dom';
0003 | import { useAuthStore } from '@/store/authStore';
0004 | import { Card } from '@/components/ui/Card';
0005 | import { Input } from '@/components/ui/Input';
0006 | import { Button } from '@/components/ui/Button';
0007 | import { useForm } from 'react-hook-form';
0008 | import { zodResolver } from '@hookform/resolvers/zod';
0009 | import * as z from 'zod';
0010 | import { UserPlus, BookOpen, AlertTriangle } from 'lucide-react';
0011 | 
0012 | const signupSchema = z.object({
0013 |   username: z.string().min(3, 'Username must be at least 3 characters').max(50),
0014 |   email: z.string().email('Please enter a valid email address'),
0015 |   password: z.string().min(8, 'Password must be at least 8 characters'),
0016 |   confirmPassword: z.string(),
0017 | }).refine((data) => data.password === data.confirmPassword, {
0018 |   message: "Passwords don't match",
0019 |   path: ['confirmPassword'],
0020 | });
0021 | 
0022 | type SignupFormInput = z.infer<typeof signupSchema>;
0023 | 
0024 | export const RegisterPage: React.FC = () => {
0025 |   const register_ = useAuthStore((state) => state.register);
0026 |   const navigate = useNavigate();
0027 |   const [apiError, setApiError] = useState<string | null>(null);
0028 |   const [loading, setLoading] = useState(false);
0029 | 
0030 |   const { register, handleSubmit, formState: { errors } } = useForm<SignupFormInput>({
0031 |     resolver: zodResolver(signupSchema),
0032 |   });
0033 | 
0034 |   const onSubmit = async (data: SignupFormInput) => {
0035 |     setLoading(true);
0036 |     setApiError(null);
0037 |     try {
0038 |       await register_(data.username, data.email, data.password);
0039 |       navigate('/');
0040 |     } catch (err: any) {
0041 |       setApiError(err?.error?.message || 'Registration failed');
0042 |     } finally {
0043 |       setLoading(false);
0044 |     }
0045 |   };
0046 | 
0047 |   return (
0048 |     <div className="max-w-md mx-auto mt-12">
0049 |       <div className="text-center mb-8">
0050 |         <BookOpen className="h-12 w-12 text-steel-500 mx-auto mb-3" />
0051 |         <h1 className="text-3xl font-extrabold tracking-tight">Create Author Account</h1>
0052 |         <p className="text-sm text-gray-500 mt-1">Register a new profile in your application database</p>
0053 |       </div>
0054 | 
0055 |       <Card className="p-6">
0056 |         {apiError && (
0057 |           <div className="flex items-center gap-2 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/40 p-3 rounded-md mb-4 text-sm text-red-600 dark:text-red-400">
0058 |             <AlertTriangle className="h-4.5 w-4.5 flex-shrink-0" />
0059 |             <span>{apiError}</span>
0060 |           </div>
0061 |         )}
0062 | 
0063 |         <form onSubmit={handleSubmit(onSubmit)}>
0064 |           <Input label="Username" placeholder="e.g. corey_schafer" {...register('username')} error={errors.username?.message} />
0065 |           <Input label="Email Address" type="email" placeholder="corey@fieldnotes.io" {...register('email')} error={errors.email?.message} />
0066 |           <Input label="Password" type="password" placeholder="At least 8 characters" {...register('password')} error={errors.password?.message} />
0067 |           <Input label="Confirm Password" type="password" {...register('confirmPassword')} error={errors.confirmPassword?.message} />
0068 | 
0069 |           <Button type="submit" className="w-full justify-center gap-1.5 mt-2" isLoading={loading}>
0070 |             <UserPlus className="h-4 w-4" />
0071 |             <span>Create Profile</span>
0072 |           </Button>
0073 |         </form>
0074 |       </Card>
0075 | 
0076 |       <div className="text-center mt-6 text-sm text-gray-500">
0077 |         Already registered?{' '}
0078 |         <Link to="/login" className="text-steel-500 hover:underline font-bold">
0079 |           Sign In
0080 |         </Link>
0081 |       </div>
0082 |     </div>
0083 |   );
0084 | };

```


================================================================================
# FILE: .\frontend\src\pages\UserProfilePage.tsx
================================================================================

```tsx
0001 | import React from 'react';
0002 | import { useParams, Link } from 'react-router-dom';
0003 | import { useUsers } from '@/hooks/useUsers';
0004 | import { usePosts } from '@/hooks/usePosts';
0005 | import { Card } from '@/components/ui/Card';
0006 | import { Terminal, Calendar, User as UserIcon } from 'lucide-react';
0007 | 
0008 | export const UserProfilePage: React.FC = () => {
0009 |   const { id } = useParams<{ id: string }>();
0010 |   const userId = Number(id);
0011 | 
0012 |   const { useGetUser } = useUsers();
0013 |   const { useGetPosts } = usePosts();
0014 | 
0015 |   const { data: user, isLoading: userLoading } = useGetUser(userId);
0016 |   const { data: posts, isLoading: postsLoading } = useGetPosts();
0017 | 
0018 |   if (userLoading || postsLoading) {
0019 |     return <div className="animate-pulse bg-white dark:bg-zinc-900 p-6 rounded-lg h-64" />;
0020 |   }
0021 | 
0022 |   if (!user) {
0023 |     return <div className="text-center p-8">Author not found.</div>;
0024 |   }
0025 | 
0026 |   // Filter all posts to only this author's — using nested user.id (not id_user)
0027 |   const userPosts = posts?.filter((p) => p.user?.id === userId) || [];
0028 | 
0029 |   return (
0030 |     <div className="space-y-6">
0031 | 
0032 |       {/* Public Profile Header — no email, no settings button */}
0033 |       <Card className="p-6">
0034 |         <div className="flex items-center gap-4">
0035 |           <div className="w-16 h-16 rounded-full bg-steel-500 text-white font-extrabold flex items-center justify-center text-2xl shadow-md border-2 border-white dark:border-zinc-800">
0036 |             {user.username.substring(0, 2).toUpperCase()}
0037 |           </div>
0038 |           <div>
0039 |             <h1 className="text-2xl font-bold flex items-center gap-1">
0040 |               <UserIcon className="h-5 w-5 text-steel-500" />
0041 |               <span>{user.username}</span>
0042 |             </h1>
0043 |             <p className="text-xs font-semibold text-steel-500 mt-2 bg-steel-100 dark:bg-zinc-800/80 px-2 py-0.5 rounded-full inline-block">
0044 |               {userPosts.length} {userPosts.length === 1 ? 'Note' : 'Notes'} Published
0045 |             </p>
0046 |           </div>
0047 |         </div>
0048 |       </Card>
0049 | 
0050 |       {/* This author's posts */}
0051 |       <div className="space-y-4">
0052 |         <h2 className="text-lg font-bold border-b border-gray-100 dark:border-zinc-800 pb-2">
0053 |           Notes by {user.username}
0054 |         </h2>
0055 | 
0056 |         {userPosts.length === 0 ? (
0057 |           <Card className="p-8 text-center text-gray-500">
0058 |             No notes written by this author yet.
0059 |           </Card>
0060 |         ) : (
0061 |           userPosts.map((post) => (
0062 |             <Card key={post.id} className="p-6">
0063 |               <div className="flex items-center gap-1.5 text-xs text-gray-500 dark:text-zinc-400 mb-2">
0064 |                 <Calendar className="h-3 w-3" />
0065 |                 <span>{new Date(post.created_at).toLocaleDateString()}</span>
0066 |               </div>
0067 |               <h3 className="text-lg font-bold mb-2">
0068 |                 <Link
0069 |                   to={`/posts/${post.id}`}
0070 |                   className="text-gray-900 dark:text-zinc-100 hover:text-steel-500"
0071 |                 >
0072 |                   {post.title}
0073 |                 </Link>
0074 |               </h3>
0075 |               <p className="text-gray-600 dark:text-zinc-300 text-sm line-clamp-3 leading-relaxed whitespace-pre-wrap">
0076 |                 {post.content}
0077 |               </p>
0078 |               <div className="mt-3">
0079 |                 <Link
0080 |                   to={`/posts/${post.id}`}
0081 |                   className="inline-flex items-center gap-1 text-xs font-bold text-steel-500 hover:underline"
0082 |                 >
0083 |                   <Terminal className="h-3.5 w-3.5" />
0084 |                   <span>Read full note</span>
0085 |                 </Link>
0086 |               </div>
0087 |             </Card>
0088 |           ))
0089 |         )}
0090 |       </div>
0091 |     </div>
0092 |   );
0093 | };

```


================================================================================
# FILE: .\frontend\src\pages\UsersPage.tsx
================================================================================

```tsx
0001 | import React from 'react';
0002 | import { useUsers } from '@/hooks/useUsers';
0003 | import { Card } from '@/components/ui/Card';
0004 | import { Link } from 'react-router-dom';
0005 | import { Users, Mail } from 'lucide-react';
0006 | 
0007 | export const UsersPage: React.FC = () => {
0008 |   const { useGetUsers } = useUsers();
0009 |   const { data: users, isLoading } = useGetUsers();
0010 | 
0011 |   if (isLoading) return <div className="text-center py-8">Loading directory...</div>;
0012 | 
0013 |   return (
0014 |     <div className="space-y-6">
0015 |       <div className="border-b border-gray-200 dark:border-zinc-800 pb-4">
0016 |         <h1 className="text-3xl font-bold flex items-center gap-2">
0017 |           <Users className="h-8 w-8 text-steel-500" />
0018 |           <span>Authors</span>
0019 |         </h1>
0020 |         <p className="text-gray-500 dark:text-zinc-400 mt-1 text-sm">Browse registered authors and their notes.</p>
0021 |       </div>
0022 | 
0023 |       <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
0024 |         {users?.map((user) => (
0025 |           <Card key={user.id} className="p-6 flex items-center gap-4">
0026 |             <div className="w-12 h-12 rounded-full bg-steel-100 dark:bg-zinc-800 text-steel-700 dark:text-zinc-300 font-bold flex items-center justify-center text-sm shadow-inner">
0027 |               {user.username.substring(0, 2).toUpperCase()}
0028 |             </div>
0029 |             <div>
0030 |               <Link to={`/users/${user.id}`} className="font-bold text-gray-900 dark:text-zinc-100 hover:text-steel-500 hover:underline">
0031 |                 {user.username}
0032 |               </Link>
0033 |             </div>
0034 |           </Card>
0035 |         ))}
0036 |       </div>
0037 |     </div>
0038 |   );
0039 | };

```


================================================================================
# FILE: .\frontend\src\store\authStore.ts
================================================================================

```ts
0001 | import { create } from 'zustand';
0002 | import { persist } from 'zustand/middleware';
0003 | import { User } from '@/types/api';
0004 | import { api } from '@/lib/api';
0005 | 
0006 | interface AuthState {
0007 |   token: string | null;
0008 |   currentUser: User | null;
0009 |   isAuthenticated: boolean;
0010 |   isInitializing: boolean;
0011 |   login: (email: string, password: string) => Promise<void>;
0012 |   register: (username: string, email: string, password: string) => Promise<void>;
0013 |   logout: () => void;
0014 |   checkAuth: () => Promise<void>;
0015 | }
0016 | 
0017 | export const useAuthStore = create<AuthState>()(
0018 |   persist(
0019 |     (set, get) => ({
0020 |       token: null,
0021 |       currentUser: null,
0022 |       isAuthenticated: false,
0023 |       isInitializing: true,
0024 | 
0025 |       login: async (email: string, password: string) => {
0026 |         // The backend expects OAuth2PasswordRequestForm: form-urlencoded, NOT JSON
0027 |         const params = new URLSearchParams();
0028 |         params.append('username', email); // backend treats "username" field as email
0029 |         params.append('password', password);
0030 | 
0031 |         const { data } = await api.post('/users/token', params, {
0032 |           headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
0033 |         });
0034 | 
0035 |         set({ token: data.access_token });
0036 |         await get().checkAuth(); // fetch and store the real user object
0037 |       },
0038 | 
0039 |       register: async (username: string, email: string, password: string) => {
0040 |         await api.post('/users', { username, email, password }); // this one IS JSON
0041 |         await get().login(email, password); // auto-login right after registering
0042 |       },
0043 | 
0044 |       logout: () => {
0045 |         set({ token: null, currentUser: null, isAuthenticated: false });
0046 |       },
0047 | 
0048 |       checkAuth: async () => {
0049 |         const token = get().token;
0050 |         if (!token) {
0051 |           set({ isAuthenticated: false, currentUser: null, isInitializing: false });
0052 |           return;
0053 |         }
0054 |         try {
0055 |           const { data } = await api.get<User>('/users/me');
0056 |           set({ currentUser: data, isAuthenticated: true, isInitializing: false });
0057 |         } catch {
0058 |           // token exists but is expired/invalid — clear everything
0059 |           set({ token: null, currentUser: null, isAuthenticated: false, isInitializing: false });
0060 |         }
0061 |       },
0062 |     }),
0063 |     {
0064 |       name: 'fieldnotes-auth',
0065 |       partialize: (state) => ({ token: state.token }), // ONLY persist the token, not currentUser
0066 |     }
0067 |   )
0068 | );

```


================================================================================
# FILE: .\frontend\src\types\api.ts
================================================================================

```ts
0001 | export interface User {
0002 |   id: number;
0003 |   username: string;
0004 |   email: string;
0005 | }
0006 | 
0007 | export interface Post {
0008 |   id: number;
0009 |   title: string;
0010 |   content: string;
0011 |   created_at: string;
0012 |   user: User; // Nested relationship
0013 | }
0014 | 
0015 | export interface UserCreate {
0016 |   username: string;
0017 |   email: string;
0018 | }
0019 | 
0020 | export interface UserUpdate {
0021 |   username?: string;
0022 |   email?: string;
0023 | }
0024 | 
0025 | export interface PostCreate {
0026 |   title: string;
0027 |   content: string;
0028 | }
0029 | 
0030 | export interface PostUpdate {
0031 |   title?: string;
0032 |   content?: string;
0033 | }
0034 | 
0035 | export interface ApiError {
0036 |   error: {
0037 |     message: string;
0038 |     status_code: number;
0039 |     details?: Array<{
0040 |       loc: Array<string | number>;
0041 |       msg: string;
0042 |       type: string;
0043 |     }>;
0044 |   };
0045 | }

```


================================================================================
# FILE: .\frontend\src\vite-env.d.ts
================================================================================

```ts
0001 | /// <reference types="vite/client" />

```


================================================================================
# FILE: .\frontend\tailwind.config.js
================================================================================

```js
0001 | /** @type {import('tailwindcss').Config} */
0002 | export default {
0003 |   content: [
0004 |     "./index.html",
0005 |     "./src/**/*.{js,ts,jsx,tsx}",
0006 |   ],
0007 |   darkMode: 'class',
0008 |   theme: {
0009 |     extend: {
0010 |       colors: {
0011 |         steel: {
0012 |           50: '#f4f7f9',
0013 |           100: '#e9eff3',
0014 |           500: '#527c9f', // Corey's classic brand color
0015 |           600: '#41637f',
0016 |           700: '#355067',
0017 |         },
0018 |         bg: {
0019 |           light: '#fafafa',
0020 |           dark: '#1a1a1a',
0021 |           cardLight: '#ffffff',
0022 |           cardDark: '#2d2d2d',
0023 |         }
0024 |       },
0025 |       fontFamily: {
0026 |         heading: ["Montserrat", "sans-serif"],
0027 |         body: ["Nunito", "sans-serif"],
0028 |       }
0029 |     },
0030 |   },
0031 |   plugins: [],
0032 | }

```


================================================================================
# FILE: .\frontend\tsconfig.json
================================================================================

```json
0001 | {
0002 |   "compilerOptions": {
0003 |     "target": "ES2020",
0004 |     "lib": ["DOM", "DOM.Iterable", "ES2020"],
0005 | 
0006 |     "module": "ESNext",
0007 |     "moduleResolution": "bundler",
0008 | 
0009 |     "jsx": "react-jsx",
0010 | 
0011 |     "strict": true,
0012 |     "skipLibCheck": true,
0013 | 
0014 |     "resolveJsonModule": true,
0015 |     "isolatedModules": true,
0016 | 
0017 |     "noEmit": true,
0018 | 
0019 |     "types": ["node"],
0020 | 
0021 |     "ignoreDeprecations": "6.0",
0022 | 
0023 |     "paths": {
0024 |       "@/*": ["./src/*"]
0025 |     }
0026 |   },
0027 |   "include": ["src", "vite.config.ts"]
0028 | }

```


================================================================================
# FILE: .\frontend\tsconfig.node.json
================================================================================

```json
0001 | {
0002 |   "compilerOptions": {
0003 |     "composite": true,
0004 |     "skipLibCheck": true,
0005 |     "module": "ESNext",
0006 |     "moduleResolution": "bundler",
0007 |     "allowSyntheticDefaultImports": true
0008 |   },
0009 |   "include": ["vite.config.ts"]
0010 | }

```


================================================================================
# FILE: .\frontend\vite.config.ts
================================================================================

```ts
0001 | import { defineConfig } from "vite";
0002 | import react from "@vitejs/plugin-react";
0003 | import { fileURLToPath, URL } from "node:url";
0004 | 
0005 | export default defineConfig({
0006 |   plugins: [react()],
0007 | 
0008 |   resolve: {
0009 |     alias: {
0010 |       "@": fileURLToPath(new URL("./src", import.meta.url)),
0011 |     },
0012 |   },
0013 | 
0014 |   server: {
0015 |     port: 5173,
0016 |     host: true,
0017 |   },
0018 | });

```


================================================================================
# FILE: .\router\__init__.py
================================================================================

```py

```


================================================================================
# FILE: .\router\posts.py
================================================================================

```py
0001 | from fastapi import  HTTPException, status , APIRouter
0002 | 
0003 | ## models + schemas + database
0004 | from schemas import PostCreate , PostResponse, PostUpdate 
0005 | import models 
0006 | from database import get_db 
0007 | 
0008 | ## Dependency injection for database session
0009 | from typing import Annotated
0010 | from fastapi import Depends
0011 | from sqlalchemy.orm import Session
0012 | from sqlalchemy import select
0013 | 
0014 | 
0015 | #Authorization
0016 | from auth import CurrentUser
0017 | 
0018 | #---------------
0019 | 
0020 | router = APIRouter()
0021 | 
0022 | 
0023 | # ---------------------------------------------------------
0024 | # GET all posts
0025 | # Public — no authentication required
0026 | # Anyone can read the feed
0027 | # ---------------------------------------------------------
0028 | @router.get("", response_model=list[PostResponse])
0029 | def get_posts(db: Annotated[Session, Depends(get_db)]):
0030 |     result = db.execute(select(models.Post))
0031 |     posts = result.scalars().all()
0032 |     return posts
0033 | 
0034 | 
0035 | # ---------------------------------------------------------
0036 | # GET /{id} — get a single post
0037 | # Public — no authentication required
0038 | # ---------------------------------------------------------
0039 | @router.get("/{id}", response_model=PostResponse)
0040 | def get_post(id: int, db: Annotated[Session, Depends(get_db)]):
0041 |     result = db.execute(select(models.Post).where(models.Post.id == id))
0042 |     post = result.scalars().first()
0043 |     if not post:
0044 |         raise HTTPException(
0045 |             status_code=status.HTTP_404_NOT_FOUND,
0046 |             detail="Post not found"
0047 |         )
0048 |     return post
0049 | 
0050 | 
0051 | # ---------------------------------------------------------
0052 | # POST — create a post
0053 | # Protected — requires valid JWT
0054 | # id_user comes from the token, NOT the request body
0055 | # A client cannot fake being another user
0056 | # ---------------------------------------------------------
0057 | @router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
0058 | def create_post(
0059 |     post: PostCreate,
0060 |     current_user: CurrentUser,
0061 |     db: Annotated[Session, Depends(get_db)],
0062 | ):
0063 |     # current_user.id is trusted because it came from our verified JWT
0064 |     # not from anything the client sent in the request body
0065 |     new_post = models.Post(
0066 |         title=post.title,
0067 |         content=post.content,
0068 |         id_user=current_user.id,
0069 |     )
0070 |     db.add(new_post)
0071 |     db.commit()
0072 |     db.refresh(new_post)
0073 |     return new_post
0074 | 
0075 | 
0076 | # ---------------------------------------------------------
0077 | # PATCH /{id} — update a post
0078 | # Protected — requires valid JWT
0079 | # Ownership check — you can only edit your own posts
0080 | # 401 = not logged in
0081 | # 403 = logged in but not the post owner
0082 | # ---------------------------------------------------------
0083 | @router.patch("/{id}", response_model=PostResponse)
0084 | def update_post(
0085 |     id: int,
0086 |     updated_post: PostUpdate,
0087 |     current_user: CurrentUser,
0088 |     db: Annotated[Session, Depends(get_db)],
0089 | ):
0090 |     result = db.execute(select(models.Post).where(models.Post.id == id))
0091 |     post = result.scalars().first()
0092 |     if not post:
0093 |         raise HTTPException(
0094 |             status_code=status.HTTP_404_NOT_FOUND,
0095 |             detail="Post not found"
0096 |         )
0097 | 
0098 |     # Ownership check
0099 |     # We compare the post's stored author ID to the authenticated user's ID
0100 |     if post.id_user != current_user.id:
0101 |         raise HTTPException(
0102 |             status_code=status.HTTP_403_FORBIDDEN,
0103 |             detail="Not authorized to update this post"
0104 |         )
0105 | 
0106 |     update_data = updated_post.model_dump(exclude_unset=True)
0107 |     for field, value in update_data.items():
0108 |         setattr(post, field, value)
0109 | 
0110 |     db.commit()
0111 |     db.refresh(post)
0112 |     return post
0113 | 
0114 | 
0115 | # ---------------------------------------------------------
0116 | # DELETE /{id} — delete a post
0117 | # Protected — requires valid JWT
0118 | # Ownership check — you can only delete your own posts
0119 | # ---------------------------------------------------------
0120 | @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
0121 | def delete_post(
0122 |     id: int,
0123 |     current_user: CurrentUser,
0124 |     db: Annotated[Session, Depends(get_db)],
0125 | ):
0126 |     result = db.execute(select(models.Post).where(models.Post.id == id))
0127 |     post = result.scalars().first()
0128 |     if not post:
0129 |         raise HTTPException(
0130 |             status_code=status.HTTP_404_NOT_FOUND,
0131 |             detail="Post not found"
0132 |         )
0133 | 
0134 |     # Ownership check
0135 |     if post.id_user != current_user.id:
0136 |         raise HTTPException(
0137 |             status_code=status.HTTP_403_FORBIDDEN,
0138 |             detail="Not authorized to delete this post"
0139 |         )
0140 | 
0141 |     db.delete(post)
0142 |     db.commit()

```


================================================================================
# FILE: .\router\users.py
================================================================================

```py
0001 | from fastapi import HTTPException, status, APIRouter
0002 | 
0003 | ## models + schemas + database
0004 | from schemas import  UserCreate, UserPrivate  , UserPublic , UserUpdate
0005 | import models 
0006 | from database import get_db 
0007 | 
0008 | ## Dependency injection for database session
0009 | from typing import Annotated
0010 | from fastapi import Depends
0011 | from sqlalchemy.orm import Session
0012 | from sqlalchemy import select
0013 | 
0014 | # Authentication
0015 | from datetime import timedelta
0016 | from fastapi.security import OAuth2PasswordRequestForm
0017 | from sqlalchemy import func, select
0018 | from auth import hash_password, create_access_token, verify_password 
0019 | from config import settings
0020 | from schemas import Token
0021 | 
0022 | 
0023 | # Authorization 
0024 | from  auth import CurrentUser
0025 | #------------
0026 | 
0027 | 
0028 | router = APIRouter()
0029 | 
0030 | 
0031 | 
0032 | 
0033 | # ---------------------------------------------------------
0034 | # GET all users
0035 | # Public — no authentication required
0036 | # Anyone can browse the author list
0037 | # ---------------------------------------------------------
0038 | @router.get("", response_model=list[UserPublic])
0039 | def get_users(db: Annotated[Session, Depends(get_db)]):
0040 |     result = db.execute(select(models.User))
0041 |     users = result.scalars().all()
0042 |     return users
0043 | 
0044 | 
0045 | # ---------------------------------------------------------
0046 | # GET /me  — must come before /{id} to avoid path conflict
0047 | # Protected — requires valid JWT
0048 | # Returns the full private profile of whoever is logged in
0049 | # Collapsed from ~20 lines to 3 using CurrentUser dependency
0050 | # ---------------------------------------------------------
0051 | @router.get("/me", response_model=UserPrivate)
0052 | def get_me(current_user: CurrentUser):
0053 |     # get_current_user already did all the work:
0054 |     # extracted the token, verified it, fetched the user from the DB
0055 |     # we just return what it gave us
0056 |     return current_user
0057 | 
0058 | 
0059 | # ---------------------------------------------------------
0060 | # GET /{id}
0061 | # Public — no authentication required
0062 | # Returns the public profile of any author
0063 | # NOTE: defined AFTER /me to avoid "me" being treated as an integer ID
0064 | # ---------------------------------------------------------
0065 | @router.get("/{id}", response_model=UserPublic)
0066 | def get_user_by_id(id: int, db: Annotated[Session, Depends(get_db)]):
0067 |     result = db.execute(select(models.User).where(models.User.id == id))
0068 |     user = result.scalars().first()
0069 |     if not user:
0070 |         raise HTTPException(
0071 |             status_code=status.HTTP_404_NOT_FOUND,
0072 |             detail="User not found"
0073 |         )
0074 |     return user
0075 | 
0076 | 
0077 | # ---------------------------------------------------------
0078 | # POST  — register a new user
0079 | # Public — no authentication required (you can't log in before registering)
0080 | # Returns UserPrivate so the new user sees their own email
0081 | # ---------------------------------------------------------
0082 | @router.post("", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
0083 | def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
0084 |     existing = db.execute(
0085 |         select(models.User).where(
0086 |             (func.lower(models.User.username) == user.username.lower())
0087 |             | (func.lower(models.User.email) == user.email.lower())
0088 |         )
0089 |     ).scalars().first()
0090 | 
0091 |     if existing:
0092 |         raise HTTPException(
0093 |             status_code=status.HTTP_400_BAD_REQUEST,
0094 |             detail="Username or email already registered"
0095 |         )
0096 | 
0097 |     new_user = models.User(
0098 |         username=user.username,
0099 |         email=user.email.lower(),
0100 |         password_hash=hash_password(user.password),
0101 |     )
0102 |     db.add(new_user)
0103 |     db.commit()
0104 |     db.refresh(new_user)
0105 |     return new_user
0106 | 
0107 | 
0108 | # ---------------------------------------------------------
0109 | # POST /token — login
0110 | # Public — this IS the authentication endpoint
0111 | # Accepts form-urlencoded data (OAuth2PasswordRequestForm)
0112 | # Returns a JWT access token on success
0113 | # ---------------------------------------------------------
0114 | @router.post("/token", response_model=Token)
0115 | def login(
0116 |     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
0117 |     db: Annotated[Session, Depends(get_db)],
0118 | ):
0119 |     # OAuth2PasswordRequestForm uses "username" field — we treat it as email
0120 |     result = db.execute(
0121 |         select(models.User).where(
0122 |             func.lower(models.User.email) == form_data.username.lower()
0123 |         )
0124 |     )
0125 |     user = result.scalars().first()
0126 | 
0127 |     # Deliberately identical error for wrong email AND wrong password
0128 |     # Never reveal which one was incorrect — prevents account enumeration
0129 |     if not user or not verify_password(form_data.password, user.password_hash):
0130 |         raise HTTPException(
0131 |             status_code=status.HTTP_401_UNAUTHORIZED,
0132 |             detail="Incorrect email or password",
0133 |         )
0134 | 
0135 |     access_token = create_access_token(
0136 |         data={"sub": str(user.id)},
0137 |         expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
0138 |     )
0139 |     return {"access_token": access_token, "token_type": "bearer"}
0140 | 
0141 | 
0142 | # ---------------------------------------------------------
0143 | # PATCH /{id} — update a user's own profile
0144 | # Protected — requires valid JWT
0145 | # Ownership check — you can only update your own account
0146 | # Returns UserPrivate so the user sees their updated email
0147 | # ---------------------------------------------------------
0148 | @router.patch("/{id}", response_model=UserPrivate)
0149 | def update_user(
0150 |     id: int,
0151 |     user_update: UserUpdate,
0152 |     current_user: CurrentUser,
0153 |     db: Annotated[Session, Depends(get_db)],
0154 | ):
0155 |     # Ownership check
0156 |     # 401 = not logged in at all
0157 |     # 403 = logged in but not the owner of this resource
0158 |     if id != current_user.id:
0159 |         raise HTTPException(
0160 |             status_code=status.HTTP_403_FORBIDDEN,
0161 |             detail="Not authorized to update this user"
0162 |         )
0163 | 
0164 |     result = db.execute(select(models.User).where(models.User.id == id))
0165 |     user = result.scalars().first()
0166 |     if not user:
0167 |         raise HTTPException(
0168 |             status_code=status.HTTP_404_NOT_FOUND,
0169 |             detail="User not found"
0170 |         )
0171 | 
0172 |     if user_update.username is not None and user_update.username.lower() != user.username.lower():
0173 |         existing = db.execute(
0174 |             select(models.User).where(
0175 |                 func.lower(models.User.username) == user_update.username.lower()
0176 |             )
0177 |         ).scalars().first()
0178 |         if existing:
0179 |             raise HTTPException(
0180 |                 status_code=status.HTTP_400_BAD_REQUEST,
0181 |                 detail="Username already exists"
0182 |             )
0183 | 
0184 |     if user_update.email is not None and user_update.email.lower() != user.email.lower():
0185 |         existing = db.execute(
0186 |             select(models.User).where(
0187 |                 func.lower(models.User.email) == user_update.email.lower()
0188 |             )
0189 |         ).scalars().first()
0190 |         if existing:
0191 |             raise HTTPException(
0192 |                 status_code=status.HTTP_400_BAD_REQUEST,
0193 |                 detail="Email already exists"
0194 |             )
0195 | 
0196 |     update_data = user_update.model_dump(exclude_unset=True)
0197 |     for field, value in update_data.items():
0198 |         if field == "email" and value is not None:
0199 |             value = value.lower()
0200 |         setattr(user, field, value)
0201 | 
0202 |     db.commit()
0203 |     db.refresh(user)
0204 |     return user
0205 | 
0206 | 
0207 | # ---------------------------------------------------------
0208 | # DELETE /{id} — delete a user's own account
0209 | # Protected — requires valid JWT
0210 | # Ownership check — you can only delete your own account
0211 | # Cascade in models.py handles deleting all their posts too
0212 | # ---------------------------------------------------------
0213 | @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
0214 | def delete_user(
0215 |     id: int,
0216 |     current_user: CurrentUser,
0217 |     db: Annotated[Session, Depends(get_db)],
0218 | ):
0219 |     # Ownership check
0220 |     if id != current_user.id:
0221 |         raise HTTPException(
0222 |             status_code=status.HTTP_403_FORBIDDEN,
0223 |             detail="Not authorized to delete this user"
0224 |         )
0225 | 
0226 |     result = db.execute(select(models.User).where(models.User.id == id))
0227 |     user = result.scalars().first()
0228 |     if not user:
0229 |         raise HTTPException(
0230 |             status_code=status.HTTP_404_NOT_FOUND,
0231 |             detail="User not found"
0232 |         )
0233 | 
0234 |     db.delete(user)
0235 |     db.commit()

```

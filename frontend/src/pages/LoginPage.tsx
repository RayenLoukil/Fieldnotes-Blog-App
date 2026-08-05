import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { BookOpen, Key, AlertTriangle } from 'lucide-react';

const loginSchema = z.object({
  username: z.string().min(1, "Please enter your username"),
});

type LoginFormInput = z.infer<typeof loginSchema>;

export const LoginPage: React.FC = () => {
  const login = useAuthStore((state) => state.login);
  const navigate = useNavigate();
  const [apiError, setApiError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormInput>({
    resolver: zodResolver(loginSchema)
  });

  const onSubmit = async (data: LoginFormInput) => {
    setLoading(true);
    setApiError(null);
    try {
      await login(data.username);
      navigate('/');
    } catch (err: any) {
      setApiError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12">
      <div className="text-center mb-8">
        <BookOpen className="h-12 w-12 text-steel-500 mx-auto mb-3" />
        <h1 className="text-3xl font-extrabold tracking-tight">Log into Fieldnotes</h1>
        <p className="text-sm text-gray-500 mt-1">Authenticate against your SQLite user directory</p>
      </div>

      <Card className="p-6">
        {apiError && (
          <div className="flex items-center gap-2 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/40 p-3 rounded-md mb-4 text-sm text-red-600 dark:text-red-400">
            <AlertTriangle className="h-4.5 w-4.5 flex-shrink-0" />
            <span>{apiError}</span>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)}>
          <Input 
            label="Username" 
            placeholder="e.g. corey_schafer" 
            {...register('username')} 
            error={errors.username?.message} 
          />

          <Button type="submit" className="w-full justify-center gap-1.5 mt-2" isLoading={loading}>
            <Key className="h-4 w-4" />
            <span>Sign In</span>
          </Button>
        </form>
      </Card>

      <div className="text-center mt-6 text-sm text-gray-500">
        New author?{' '}
        <Link to="/signup" className="text-steel-500 hover:underline font-bold">
          Register new account
        </Link>
      </div>
    </div>
  );
};
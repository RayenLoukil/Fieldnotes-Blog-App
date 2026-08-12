import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { UserPlus, BookOpen, AlertTriangle } from 'lucide-react';

const signupSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters').max(50),
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type SignupFormInput = z.infer<typeof signupSchema>;

export const RegisterPage: React.FC = () => {
  const register_ = useAuthStore((state) => state.register);
  const navigate = useNavigate();
  const [apiError, setApiError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<SignupFormInput>({
    resolver: zodResolver(signupSchema),
  });

  const onSubmit = async (data: SignupFormInput) => {
    setLoading(true);
    setApiError(null);
    try {
      await register_(data.username, data.email, data.password);
      navigate('/');
    } catch (err: any) {
      setApiError(err?.error?.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12">
      <div className="text-center mb-8">
        <BookOpen className="h-12 w-12 text-steel-500 mx-auto mb-3" />
        <h1 className="text-3xl font-extrabold tracking-tight">Create Author Account</h1>
        <p className="text-sm text-gray-500 mt-1">Register a new profile in your application database</p>
      </div>

      <Card className="p-6">
        {apiError && (
          <div className="flex items-center gap-2 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/40 p-3 rounded-md mb-4 text-sm text-red-600 dark:text-red-400">
            <AlertTriangle className="h-4.5 w-4.5 flex-shrink-0" />
            <span>{apiError}</span>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)}>
          <Input label="Username" placeholder="e.g. john_doe" {...register('username')} error={errors.username?.message} />
          <Input label="Email Address" type="email" placeholder="you@example.com" {...register('email')} error={errors.email?.message} />
          <Input label="Password" type="password" placeholder="At least 8 characters" {...register('password')} error={errors.password?.message} />
          <Input label="Confirm Password" type="password" placeholder="Re-enter your password" {...register('confirmPassword')} error={errors.confirmPassword?.message} />

          <Button type="submit" className="w-full justify-center gap-1.5 mt-2" isLoading={loading}>
            <UserPlus className="h-4 w-4" />
            <span>Create Profile</span>
          </Button>
        </form>
      </Card>

      <div className="text-center mt-6 text-sm text-gray-500">
        Already registered?{' '}
        <Link to="/login" className="text-steel-500 hover:underline font-bold">
          Sign In
        </Link>
      </div>
    </div>
  );
};
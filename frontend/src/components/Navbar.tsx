import React, { useEffect, useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { BookOpen, Moon, Sun, Users, PlusCircle, LogOut, User } from 'lucide-react';
import { Button } from './ui/Button';

interface NavbarProps {
  onCreatePostClick: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onCreatePostClick }) => {
  const { currentUser, logout, isAuthenticated } = useAuthStore();
  const navigate = useNavigate();
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light');

  useEffect(() => {
    const root = window.document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-40 bg-steel-500 text-white shadow-md">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        
        {/* Brand */}
        <Link to="/" className="flex items-center gap-2 text-xl font-bold tracking-tight text-white hover:opacity-90">
          <BookOpen className="h-6 w-6" />
          <span>Fieldnotes</span>
        </Link>

        {/* Action Controls */}
        <div className="flex items-center gap-5">
          {isAuthenticated && (
            <div className="flex items-center gap-4 text-sm font-medium">
              <NavLink 
                to="/" 
                className={({ isActive }) => `hover:text-steel-100 transition-colors ${isActive ? 'underline underline-offset-4 decoration-2 font-bold text-white' : 'text-steel-100'}`}
              >
                Feed
              </NavLink>
              <NavLink 
                to="/users" 
                className={({ isActive }) => `hover:text-steel-100 transition-colors ${isActive ? 'underline underline-offset-4 decoration-2 font-bold text-white' : 'text-steel-100'}`}
              >
                Authors
              </NavLink>
            </div>
          )}

          {isAuthenticated && <div className="h-6 w-[1px] bg-steel-600 hidden sm:block" />}

          <div className="flex items-center gap-3">
            {isAuthenticated && (
              <Button 
                onClick={onCreatePostClick}
                className="bg-white/10 hover:bg-white/20 border border-white/20 text-white gap-2"
                size="sm"
              >
                <PlusCircle className="h-4 w-4" />
                <span className="hidden sm:inline">Write Note</span>
              </Button>
            )}

            <button
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              className="p-2 hover:bg-steel-600 rounded-full transition-colors text-white"
              title="Toggle view theme"
            >
              {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            </button>

            {isAuthenticated && currentUser && (
              <>
                <Link 
                  to={`/users/${currentUser.id}`} 
                  className="flex items-center gap-2 hover:bg-steel-600 p-1.5 rounded-full transition-colors"
                  title="My Profile Settings"
                >
                  <div className="w-8 h-8 rounded-full bg-steel-100 text-steel-700 font-extrabold flex items-center justify-center text-sm shadow-sm">
                    {currentUser.username.substring(0, 2).toUpperCase()}
                  </div>
                </Link>

                <button
                  onClick={handleLogout}
                  className="p-2 hover:bg-steel-600 rounded-full transition-colors text-white"
                  title="Log Out Session"
                >
                  <LogOut className="h-5 w-5" />
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};
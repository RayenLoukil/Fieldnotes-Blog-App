import React, { useState } from 'react';
import { getImageUrl } from '@/lib/api';

interface AvatarProps {
  username: string;
  imagePath?: string | null;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const sizeMap = {
  sm: 'w-8 h-8 text-xs',
  md: 'w-12 h-12 text-sm',
  lg: 'w-16 h-16 text-xl',
};

export const Avatar: React.FC<AvatarProps> = ({ username, imagePath, size = 'md', className = '' }) => {
  const [failed, setFailed] = useState(false);
  const initials = username.substring(0, 2).toUpperCase();
  const showImage = imagePath && !failed;

  return (
    <div
      className={`rounded-full overflow-hidden flex items-center justify-center flex-shrink-0 bg-steel-100 dark:bg-zinc-800 text-steel-700 dark:text-steel-300 font-extrabold shadow-inner border border-gray-100 dark:border-zinc-750 ${sizeMap[size]} ${className}`}
    >
      {showImage ? (
        <img
          src={getImageUrl(imagePath)}
          alt={username}
          className="w-full h-full object-cover"
          onError={() => setFailed(true)}
        />
      ) : (
        <span>{initials}</span>
      )}
    </div>
  );
};
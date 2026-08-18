import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useUsers } from '@/hooks/useUsers';
import { usePosts } from '@/hooks/usePosts';
import { Card } from '@/components/ui/Card';
import { Avatar } from '@/components/ui/Avatar';
import { Terminal, Calendar, User as UserIcon } from 'lucide-react';

export const UserProfilePage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const userId = Number(id);

  const { useGetUser } = useUsers();
  const { useGetUserPosts } = usePosts();

  const { data: user, isLoading: userLoading } = useGetUser(userId);
  const { data: userPosts = [], isLoading: postsLoading } = useGetUserPosts(userId);

  if (userLoading || postsLoading) {
    return <div className="animate-pulse bg-white dark:bg-zinc-900 p-6 rounded-lg h-64" />;
  }

  if (!user) {
    return <div className="text-center p-8">Author not found.</div>;
  }



  return (
    <div className="space-y-6">

      {/* Public Profile Header — no email, no settings button */}
      <Card className="p-6">
        <div className="flex items-center gap-4">
          <Avatar username={user.username} imagePath={user.image_path} size="lg" />
          <div>
            <h1 className="text-2xl font-bold flex items-center gap-1">
              <UserIcon className="h-5 w-5 text-steel-500" />
              <span>{user.username}</span>
            </h1>
            <p className="text-xs font-semibold text-steel-500 mt-2 bg-steel-100 dark:bg-zinc-800/80 px-2 py-0.5 rounded-full inline-block">
              {userPosts.length} {userPosts.length === 1 ? 'Note' : 'Notes'} Published
            </p>
          </div>
        </div>
      </Card>

      {/* This author's posts */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold border-b border-gray-100 dark:border-zinc-800 pb-2">
          Notes by {user.username}
        </h2>

        {userPosts.length === 0 ? (
          <Card className="p-8 text-center text-gray-500">
            No notes written by this author yet.
          </Card>
        ) : (
          userPosts.map((post) => (
            <Card key={post.id} className="p-6">
              <div className="flex items-center gap-1.5 text-xs text-gray-500 dark:text-zinc-400 mb-2">
                <Calendar className="h-3 w-3" />
                <span>{new Date(post.created_at).toLocaleDateString()}</span>
              </div>
              <h3 className="text-lg font-bold mb-2">
                <Link
                  to={`/posts/${post.id}`}
                  className="text-gray-900 dark:text-zinc-100 hover:text-steel-500"
                >
                  {post.title}
                </Link>
              </h3>
              <p className="text-gray-600 dark:text-zinc-300 text-sm line-clamp-3 leading-relaxed whitespace-pre-wrap">
                {post.content}
              </p>
              <div className="mt-3">
                <Link
                  to={`/posts/${post.id}`}
                  className="inline-flex items-center gap-1 text-xs font-bold text-steel-500 hover:underline"
                >
                  <Terminal className="h-3.5 w-3.5" />
                  <span>Read full note</span>
                </Link>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};
import React from 'react';
import { Link } from 'react-router-dom';
import { usePosts } from '@/hooks/usePosts';
import { Card } from '@/components/ui/Card';
import { Avatar } from '@/components/ui/Avatar';
import { AlertCircle, Calendar, MessageSquare, Terminal } from 'lucide-react';

export const FeedPage: React.FC = () => {
  const { useGetPostsInfinite } = usePosts();
  const {
    data,
    isLoading,
    error,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useGetPostsInfinite();

  const posts = data?.pages.flatMap((page) => page.posts) ?? [];

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((n) => (
          <div key={n} className="animate-pulse bg-white dark:bg-zinc-900 border border-gray-255 dark:border-zinc-800 p-6 rounded-lg">
            <div className="flex items-center gap-4 mb-4">
              <div className="w-12 h-12 bg-gray-200 dark:bg-zinc-800 rounded-full" />
              <div className="flex-1 space-y-2">
                <div className="h-4 bg-gray-200 dark:bg-zinc-800 rounded w-1/4" />
                <div className="h-3 bg-gray-200 dark:bg-zinc-800 rounded w-1/6" />
              </div>
            </div>
            <div className="h-6 bg-gray-200 dark:bg-zinc-800 rounded w-3/4 mb-3" />
            <div className="h-4 bg-gray-200 dark:bg-zinc-800 rounded w-full" />
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center p-8 text-center bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/30 rounded-lg">
        <AlertCircle className="h-12 w-12 text-red-500 mb-2" />
        <h3 className="text-lg font-semibold text-red-800 dark:text-red-200">Error Connecting to Backend</h3>
        <p className="text-sm text-red-600 dark:text-red-400 mt-1">Make sure uvicorn is running on port 8000.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 dark:border-zinc-850 pb-4">
        <h1 className="text-3xl font-extrabold flex items-center gap-2">
          <Terminal className="h-8 w-8 text-steel-500" />
          <span>Latest Notes</span>
        </h1>
        <p className="text-gray-500 dark:text-zinc-400 mt-1 text-sm">A collaborative technical diary of design logs, commands, and notes.</p>
      </div>

      {posts && posts.length === 0 ? (
        <Card className="p-8 text-center">
          <MessageSquare className="h-12 w-12 text-gray-300 mx-auto mb-2" />
          <p className="text-gray-500 dark:text-zinc-400">No logs posted yet. Be the first to share your field notes!</p>
        </Card>
      ) : (
        <div className="space-y-4">
          {posts.map((post) => (
            <Card key={post.id} className="p-6">
              <article className="flex flex-col sm:flex-row items-start gap-4">
                
                <Link to={`/users/${post.user?.id}`} className="flex-shrink-0">
                  <Avatar username={post.user?.username || 'UN'} imagePath={post.user?.image_path} size="md" />
                </Link>

                <div className="flex-grow">
                  <div className="flex flex-wrap items-center gap-2 text-xs text-gray-500 dark:text-zinc-400 mb-2 border-b border-gray-100 dark:border-zinc-800/80 pb-2">
                    <Link to={`/users/${post.user?.id}`} className="font-bold text-steel-500 hover:underline">
                      {post.user?.username || "Anonymous"}
                    </Link>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <Calendar className="h-3 w-3" />
                      {new Date(post.created_at).toLocaleDateString(undefined, {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric'
                      })}
                    </span>
                  </div>

                  <h2 className="text-xl font-bold mb-2">
                    <Link to={`/posts/${post.id}`} className="text-gray-900 dark:text-zinc-100 hover:text-steel-500 transition-colors">
                      {post.title}
                    </Link>
                  </h2>

                  <p className="text-gray-600 dark:text-zinc-300 line-clamp-3 text-sm leading-relaxed whitespace-pre-wrap">
                    {post.content}
                  </p>

                  <div className="mt-4">
                    <Link to={`/posts/${post.id}`} className="text-xs font-bold text-steel-500 hover:text-steel-600">
                      Read full entry →
                    </Link>
                  </div>
                </div>

              </article>
            </Card>
          ))}

          {hasNextPage && (
            <div className="flex justify-center pt-4">
              <button
                onClick={() => fetchNextPage()}
                disabled={isFetchingNextPage}
                className="px-4 py-2 text-sm font-bold text-steel-500 hover:text-steel-600 border border-steel-200 dark:border-zinc-700 rounded-md hover:bg-steel-50 dark:hover:bg-zinc-800 transition-colors disabled:opacity-50"
              >
                {isFetchingNextPage ? 'Loading...' : 'Load More Posts'}
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
'use client';

import { useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

export default function Callback() {
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const code = searchParams.get('code');
    if (!code) {
      router.push('/');
      return;
    }

    // Exchange code for token
    fetch(`/api/spotify?action=callback&code=${code}`)
      .then(res => res.json())
      .then(data => {
        if (data.token) {
          localStorage.setItem('spotify_token', data.token);
          router.push('/');
        } else {
          console.error('Failed to get token:', data.error);
          router.push('/');
        }
      })
      .catch(error => {
        console.error('Error during authentication:', error);
        router.push('/');
      });
  }, [router, searchParams]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">Completing Authentication...</h1>
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
      </div>
    </div>
  );
} 
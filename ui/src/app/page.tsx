'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [artists, setArtists] = useState<string[]>([]);
  const [newArtist, setNewArtist] = useState('');
  const [schedule, setSchedule] = useState({
    type: 'daily',
    time: '00:00',
    day: 'monday'
  });
  const router = useRouter();

  useEffect(() => {
    // Check if we have a token in localStorage
    // const token = localStorage.getItem('spotify_token');
    // if (token) {
    //   setIsAuthenticated(true);
    //   loadArtists();
    // } else {
    //   // Start authentication flow
    //   fetch('/api/spotify?action=auth')
    //     .then(res => res.json())
    //     .then(data => {
    //       window.location.href = data.url;
    //     })
    //     .catch(error => {
    //       console.error('Authentication error:', error);
    //     });
    // }
    setIsAuthenticated(true);
  }, []);

  const loadArtists = async () => {
    try {
      const response = await fetch('/api/spotify?action=artists');
      const data = await response.json();
      setArtists(data.artists?.items?.map((artist: any) => artist.name) || []);
    } catch (error) {
      console.error('Error loading artists:', error);
    }
  };

  const handleAddArtist = async () => {
    if (!newArtist) return;
    
    try {
      await fetch('/api/spotify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'add-artist',
          data: { artist: newArtist }
        })
      });
      
      setArtists([...artists, newArtist]);
      setNewArtist('');
    } catch (error) {
      console.error('Error adding artist:', error);
    }
  };

  const handleRemoveArtist = async (artist: string) => {
    try {
      await fetch('/api/spotify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'remove-artist',
          data: { artist }
        })
      });
      
      setArtists(artists.filter(a => a !== artist));
    } catch (error) {
      console.error('Error removing artist:', error);
    }
  };

  const handleScheduleUpdate = async () => {
    try {
      await fetch('/api/spotify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'update-schedule',
          data: schedule
        })
      });
    } catch (error) {
      console.error('Error updating schedule:', error);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Connecting to Spotify...</h1>
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-8">Spotify Playlist Generator</h1>
        
        {/* Artists Section */}
        <section className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Monitored Artists</h2>
          <div className="flex gap-2 mb-4">
            <input
              type="text"
              value={newArtist}
              onChange={(e) => setNewArtist(e.target.value)}
              placeholder="Add new artist"
              className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleAddArtist}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Add
            </button>
          </div>
          <div className="space-y-2">
            {artists.map((artist) => (
              <div key={artist} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span>{artist}</span>
                <button
                  onClick={() => handleRemoveArtist(artist)}
                  className="text-red-500 hover:text-red-700"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        </section>

        {/* Schedule Section */}
        <section className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Schedule Settings</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Schedule Type
              </label>
              <select
                value={schedule.type}
                onChange={(e) => setSchedule({ ...schedule, type: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="hourly">Hourly</option>
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
              </select>
            </div>

            {schedule.type !== 'hourly' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Time
                </label>
                <input
                  type="time"
                  value={schedule.time}
                  onChange={(e) => setSchedule({ ...schedule, time: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            )}

            {schedule.type === 'weekly' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Day of Week
                </label>
                <select
                  value={schedule.day}
                  onChange={(e) => setSchedule({ ...schedule, day: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="monday">Monday</option>
                  <option value="tuesday">Tuesday</option>
                  <option value="wednesday">Wednesday</option>
                  <option value="thursday">Thursday</option>
                  <option value="friday">Friday</option>
                  <option value="saturday">Saturday</option>
                  <option value="sunday">Sunday</option>
                </select>
              </div>
            )}

            <button
              onClick={handleScheduleUpdate}
              className="w-full px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              Update Schedule
            </button>
          </div>
        </section>
      </div>
    </main>
  );
}

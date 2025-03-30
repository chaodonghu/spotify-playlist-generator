import { NextResponse } from "next/server";

const SPOTIFY_API_BASE = 'https://api.spotify.com/v1';

async function getAccessToken() {
  const clientId = process.env.SPOTIFY_CLIENT_ID;
  const clientSecret = process.env.SPOTIFY_CLIENT_SECRET;

  const response = await fetch('https://accounts.spotify.com/api/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      Authorization: `Basic ${Buffer.from(`${clientId}:${clientSecret}`).toString('base64')}`,
    },
    body: 'grant_type=client_credentials',
  });

  const data = await response.json();
  return data.access_token;
}

async function makeSpotifyRequest(endpoint: string, options: RequestInit = {}) {
  const token = await getAccessToken();
  
  const response = await fetch(`${SPOTIFY_API_BASE}${endpoint}`, {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Spotify API error: ${response.status}`);
  }

  return response.json();
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const action = searchParams.get("action");

  try {
    switch (action) {
      case "auth":
        const clientId = process.env.SPOTIFY_CLIENT_ID;
        const redirectUri = process.env.SPOTIFY_REDIRECT_URI;
        const scope = "playlist-modify-public playlist-read-private user-read-email user-read-private";
        
        const authUrl = `https://accounts.spotify.com/authorize?client_id=${clientId}&response_type=code&redirect_uri=${encodeURIComponent(redirectUri!)}&scope=${encodeURIComponent(scope)}`;
        return NextResponse.json({ url: authUrl });

      case "callback":
        const code = searchParams.get("code");
        if (!code) {
          return NextResponse.json(
            { error: "No code provided" },
            { status: 400 }
          );
        }

        const tokenResponse = await fetch('https://accounts.spotify.com/api/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            Authorization: `Basic ${Buffer.from(`${process.env.SPOTIFY_CLIENT_ID}:${process.env.SPOTIFY_CLIENT_SECRET}`).toString('base64')}`,
          },
          body: new URLSearchParams({
            grant_type: 'authorization_code',
            code,
            redirect_uri: process.env.SPOTIFY_REDIRECT_URI!,
          }),
        });

        const tokenData = await tokenResponse.json();
        return NextResponse.json({ token: tokenData });

      case "artists":
        const artists = await makeSpotifyRequest('/search?q=artist&type=artist&limit=50');
        return NextResponse.json(artists);

      case "playlist":
        const playlistId = process.env.SPOTIFY_PLAYLIST_ID;
        if (!playlistId) {
          return NextResponse.json({ error: 'Playlist ID not configured' }, { status: 400 });
        }
        const playlist = await makeSpotifyRequest(`/playlists/${playlistId}`);
        return NextResponse.json(playlist);

      default:
        return NextResponse.json({ error: "Invalid action" }, { status: 400 });
    }
  } catch (error) {
    console.error("Spotify API error:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  const body = await request.json();
  const { action } = body;

  try {
    switch (action) {
      case "add-artist":
        // Add artist to monitoring list
        return NextResponse.json({ success: true });

      case "remove-artist":
        // Remove artist from monitoring list
        return NextResponse.json({ success: true });

      case "update-schedule":
        // Update monitoring schedule
        return NextResponse.json({ success: true });

      default:
        return NextResponse.json({ error: "Invalid action" }, { status: 400 });
    }
  } catch (error) {
    console.error("Spotify API error:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}

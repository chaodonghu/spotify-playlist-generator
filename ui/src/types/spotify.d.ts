declare module 'spotify' {
  export class Spotify {
    constructor(config: { auth: SpotifyOAuth });
    getAuthUrl(): string;
    getAccessToken(code: string): Promise<{ access_token: string; refresh_token: string }>;
    search(query: string, options: { type: string }): Promise<{
      artists: {
        items: Array<{
          name: string;
          id: string;
        }>;
      };
    }>;
    getPlaylist(playlistId: string): Promise<{
      name: string;
      tracks: {
        items: Array<{
          track: {
            name: string;
            artists: Array<{ name: string }>;
          };
        }>;
      };
    }>;
  }

  export class SpotifyOAuth {
    constructor(config: {
      clientId: string;
      clientSecret: string;
      redirectUri: string;
      scope: string;
    });
  }
} 
export interface UserProfile {
  id: string;
  name: string;
  email: string;
  avatar_url?: string;
  organization?: string;
}

export interface AuthResponse {
  token: string;
  expires_at?: string;
  user: UserProfile;
}

export interface AuthState {
  token: string | null;
  user: UserProfile | null;
  expiresAt: string | null;
}

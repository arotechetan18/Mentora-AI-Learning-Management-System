// src/api/profile.ts
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    }
  };
};

export interface Profile {
  id: number;
  user_id: number;
  bio?: string;
  phone?: string;
  location?: string;
  website?: string;
  education?: string;
  experience?: string;
  skills?: string;
  github?: string;
  linkedin?: string;
  twitter?: string;
  youtube?: string;
  avatar_url?: string;
  email_notifications: boolean;
  course_updates: boolean;
  created_at: string;
  updated_at?: string;
}

export interface UserWithProfile {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  profile?: Profile;
}

export const getMyProfile = async (): Promise<UserWithProfile> => {
  const response = await axios.get(`${API_URL}/profile/me`, getAuthHeaders());
  return response.data;
};

export const updateMyProfile = async (data: Partial<Profile>): Promise<Profile> => {
  const response = await axios.put(`${API_URL}/profile/me`, data, getAuthHeaders());
  return response.data;
};
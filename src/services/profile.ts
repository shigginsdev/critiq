import { getAuthToken } from './auth'

const PROFILE_API_URL = import.meta.env.VITE_GET_PROFILE_API_URL

export interface UserProfile {
  userId: string
  email: string
  displayName: string
  bio: string
  avatarUrl: string
  artistWebsite: string
  instagramHandle: string
}

export async function getUserProfile(): Promise<UserProfile> {
  if (!PROFILE_API_URL) {
    throw new Error('The profile API URL has not been configured.')
  }

  const token = await getAuthToken()

  const response = await fetch(PROFILE_API_URL, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!response.ok) {
    throw new Error('Unable to load user profile')
  }

  return response.json()
}

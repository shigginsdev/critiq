import { getAuthToken } from './auth'

const PROFILE_API_URL = 'https://4h2ydmma65.execute-api.us-east-2.amazonaws.com/dev'

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

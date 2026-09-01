import { getAuthToken } from '@/services/auth'

const GALLERY_API_URL = 'your-api-url'

export async function getGallery() {
  const token = await getAuthToken()

  const response = await fetch(GALLERY_API_URL, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!response.ok) {
    throw new Error(`Gallery request failed with status ${response.status}`)
  }

  return response.json()
}

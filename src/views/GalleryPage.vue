<template>
  <main class="gallery-page">
    <header class="gallery-header">
      <h1>Critique Gallery</h1>
      <p>Real gallery data from DynamoDB</p>
    </header>

    <p v-if="isLoading" class="gallery-message">Loading gallery...</p>

    <p v-else-if="errorMessage" class="gallery-error">
      {{ errorMessage }}
    </p>

    <section v-else-if="artworks.length" class="gallery-grid">
      <article v-for="artwork in artworks" :key="artwork.galleryItemId" class="gallery-card">
        <img
          :src="artwork.thumbnailUrl || artwork.imageUrl"
          :alt="artwork.title"
          class="gallery-image"
        />

        <div class="gallery-info">
          <h2>{{ artwork.title }}</h2>
          <p>{{ formatArtworkDate(artwork.artworkDate) }}</p>
        </div>
      </article>
    </section>

    <p v-else class="gallery-message">No gallery items found.</p>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
//import { fetchAuthSession } from 'aws-amplify/auth'
import { getAuthToken } from '@/services/auth'

defineOptions({
  name: 'GalleryPage',
})

const API_URL = 'https://wm8znkb2f6.execute-api.us-east-2.amazonaws.com/dev/gallery'

const artworks = ref([])
const isLoading = ref(false)
const errorMessage = ref('')

async function loadGallery() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const session = await getAuthToken()
    const token = session.tokens?.idToken?.toString()

    console.log('Has token?', !!token)

    const response = await fetch(API_URL, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error(`Gallery request failed with status ${response.status}`)
    }

    const data = await response.json()

    artworks.value = data
  } catch (error) {
    console.error('Error loading gallery:', error)
    errorMessage.value = 'Unable to load gallery items right now.'
  } finally {
    isLoading.value = false
  }
}

function formatArtworkDate(dateValue) {
  if (!dateValue) {
    return ''
  }

  const date = new Date(dateValue)

  return date.toLocaleDateString('en-US', {
    month: 'short',
    year: 'numeric',
  })
}

onMounted(() => {
  loadGallery()
})
</script>

<style scoped>
.gallery-page {
  padding: 32px;
}

.gallery-header {
  margin-bottom: 24px;
}

.gallery-header h1 {
  margin: 0;
  font-size: 2rem;
}

.gallery-header p {
  margin-top: 6px;
  color: #666;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.gallery-card {
  border: 1px solid #ddd;
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
}

.gallery-image {
  width: 100%;
  height: 160px;
  object-fit: cover;
  display: block;
}

.gallery-info {
  padding: 12px;
}

.gallery-info h2 {
  margin: 0;
  font-size: 1rem;
}

.gallery-info p {
  margin: 4px 0 0;
  font-size: 0.875rem;
  color: #777;
}

.gallery-message,
.gallery-error {
  margin-top: 24px;
  font-size: 1rem;
}

.gallery-error {
  color: #b00020;
}

@media (max-width: 900px) {
  .gallery-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 520px) {
  .gallery-grid {
    grid-template-columns: 1fr;
  }
}
</style>

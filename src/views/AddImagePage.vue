<template>
  <main class="add-image-page">
    <section class="image-card">
      <h1>Add Image</h1>
      <p>Add artwork using a publicly accessible image URL. Image uploads are not available yet.</p>
      <form @submit.prevent="saveImage">
        <fieldset :disabled="isSaving">
          <div class="form-group">
            <label for="title">Title (required)</label>
            <input id="title" v-model.trim="form.title" required maxlength="200" />
          </div>
          <div v-for="field in urlFields" :key="field.key" class="form-group">
            <label :for="field.key">{{ field.label }}</label>
            <input
              :id="field.key"
              v-model.trim="form[field.key]"
              type="url"
              :required="field.key === 'imageUrl'"
              pattern="https?://.+"
              maxlength="2048"
              placeholder="https://example.com/image.jpg"
            />
          </div>
          <p class="hint">Leave medium and thumbnail URLs blank to use the main image URL.</p>
          <div class="form-group">
            <label for="description">Description</label>
            <textarea id="description" v-model.trim="form.description" rows="5" maxlength="2000" />
          </div>
          <div class="form-group">
            <label for="artworkDate">Artwork date</label>
            <input id="artworkDate" v-model="form.artworkDate" type="date" />
          </div>
          <div class="form-group">
            <label for="tags">Tags</label>
            <input id="tags" v-model="tags" aria-describedby="tags-help" />
            <small id="tags-help"
              >Separate tags with commas. Up to 20 tags, 50 characters each.</small
            >
          </div>
          <button type="submit">{{ isSaving ? 'Saving...' : 'Save Image' }}</button>
        </fieldset>
        <p v-if="statusMessage" role="status" :class="{ error: hasError }">{{ statusMessage }}</p>
        <RouterLink to="/gallery">Back to gallery</RouterLink>
      </form>
    </section>
  </main>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { getAuthToken } from '@/services/auth'

const emptyForm = () => ({
  title: '',
  imageUrl: '',
  mediumImageUrl: '',
  thumbnailUrl: '',
  sourcePageUrl: '',
  description: '',
  artworkDate: '',
})
const form = reactive(emptyForm())
const urlFields = [
  { key: 'imageUrl', label: 'Image URL (required)' },
  { key: 'mediumImageUrl', label: 'Medium image URL' },
  { key: 'thumbnailUrl', label: 'Thumbnail URL' },
  { key: 'sourcePageUrl', label: 'Source page URL' },
] as const
const tags = ref('')
const isSaving = ref(false)
const statusMessage = ref('')
const hasError = ref(false)

async function saveImage() {
  if (isSaving.value) return
  statusMessage.value = ''
  hasError.value = false
  isSaving.value = true
  try {
    const url = import.meta.env.VITE_ADD_IMAGE_API_URL
    if (!url) throw new Error('The add image API URL has not been configured.')
    if (!form.title.trim()) throw new Error('Please enter a title.')
    const normalizedTags = [
      ...new Set(
        tags.value
          .split(',')
          .map((tag) => tag.trim())
          .filter(Boolean),
      ),
    ]
    if (normalizedTags.length > 20 || normalizedTags.some((tag) => tag.length > 50)) {
      throw new Error('Use up to 20 tags, with no more than 50 characters each.')
    }
    const token = await getAuthToken()
    const response = await fetch(url, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, tags: normalizedTags }),
    })
    const body = await response.json().catch(() => null)
    if (!response.ok) throw new Error(body?.message ?? 'Unable to save your image.')
    Object.assign(form, emptyForm())
    tags.value = ''
    statusMessage.value = 'Your image was added to the gallery.'
  } catch (error) {
    hasError.value = true
    statusMessage.value = error instanceof Error ? error.message : 'Unable to save your image.'
  } finally {
    isSaving.value = false
  }
}
</script>

<style scoped>
.add-image-page {
  display: flex;
  justify-content: center;
  padding: 2rem 1rem;
}
.image-card {
  width: 100%;
  max-width: 700px;
  padding: 2rem;
  border: 1px solid #d3d3d3;
  border-radius: 8px;
  background: white;
  box-shadow: 0 4px 12px rgb(0 0 0 / 8%);
}
h1 {
  margin-top: 0;
}
fieldset {
  padding: 0;
  margin: 1.5rem 0;
  border: 0;
  min-width: 0;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}
label {
  font-weight: 600;
}
input,
textarea {
  box-sizing: border-box;
  width: 100%;
  padding: 0.75rem;
  font: inherit;
  border: 1px solid #aaa;
  border-radius: 4px;
  color: #222;
  background: white;
}
textarea {
  resize: vertical;
}
small,
.hint {
  color: #555;
}
button {
  padding: 0.7rem 1.25rem;
  color: white;
  background: #3f3f3f;
  border: 0;
  border-radius: 4px;
  font: inherit;
  cursor: pointer;
}
fieldset:disabled button {
  opacity: 0.65;
  cursor: wait;
}
input:focus-visible,
textarea:focus-visible,
button:focus-visible,
a:focus-visible {
  outline: 3px solid #8ab4f8;
  outline-offset: 2px;
}
.error {
  color: #a40000;
}
@media (max-width: 640px) {
  .image-card {
    padding: 1.25rem;
  }
}
</style>

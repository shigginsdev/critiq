<template>
  <main class="profile-page">
    <section class="profile-card">
      <div class="profile-heading">
        <h1>Profile</h1>
        <p>Tell the Critiq community a little about yourself and your artwork.</p>
      </div>

      <form class="profile-form" @submit.prevent="saveProfile">
        <div class="form-group">
          <label for="displayName">Display name</label>
          <input
            id="displayName"
            v-model.trim="profile.displayName"
            type="text"
            maxlength="100"
            autocomplete="name"
          />
        </div>

        <div class="form-group">
          <label for="artistWebsite">Artist website</label>
          <input
            id="artistWebsite"
            v-model.trim="profile.artistWebsite"
            type="url"
            placeholder="https://example.com"
            autocomplete="url"
          />
        </div>

        <div class="form-group">
          <label for="instagramHandle">Instagram handle</label>

          <div class="instagram-input">
            <span aria-hidden="true">@</span>

            <input
              id="instagramHandle"
              v-model.trim="profile.instagramHandle"
              type="text"
              maxlength="30"
              placeholder="yourhandle"
              autocomplete="off"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="avatarUrl">Avatar image URL</label>
          <input
            id="avatarUrl"
            v-model.trim="profile.avatarUrl"
            type="url"
            placeholder="https://example.com/avatar.jpg"
          />

          <img
            v-if="profile.avatarUrl"
            class="avatar-preview"
            :src="profile.avatarUrl"
            alt="Avatar preview"
            @error="avatarLoadFailed = true"
            @load="avatarLoadFailed = false"
          />

          <p v-if="avatarLoadFailed" class="field-error">The avatar image could not be loaded.</p>
        </div>

        <div class="form-group">
          <label for="bio">Bio</label>
          <textarea
            id="bio"
            v-model.trim="profile.bio"
            rows="6"
            maxlength="1000"
            placeholder="Share a little about your artwork, experience, or creative interests."
          />

          <p class="character-count">{{ profile.bio.length }} / 1000</p>
        </div>

        <p v-if="statusMessage" class="status-message" :class="{ error: hasError }" role="status">
          {{ statusMessage }}
        </p>

        <div class="form-actions">
          <button class="save-button" type="submit" :disabled="isSaving">
            {{ isSaving ? 'Saving...' : 'Save Profile' }}
          </button>
        </div>
      </form>
    </section>
  </main>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { getAuthToken } from '@/services/auth'

interface ProfileForm {
  displayName: string
  artistWebsite: string
  bio: string
  avatarUrl: string
  instagramHandle: string
}

const profile = reactive<ProfileForm>({
  displayName: '',
  artistWebsite: '',
  bio: '',
  avatarUrl: '',
  instagramHandle: '',
})

const isSaving = ref(false)
const statusMessage = ref('')
const hasError = ref(false)
const avatarLoadFailed = ref(false)

const updateProfileApiUrl = import.meta.env.VITE_UPDATE_PROFILE_API_URL

const normalizeInstagramHandle = (handle: string): string => {
  return handle.replace(/^@/, '').trim()
}

const saveProfile = async () => {
  statusMessage.value = ''
  hasError.value = false

  if (!updateProfileApiUrl) {
    hasError.value = true
    statusMessage.value = 'The profile API URL has not been configured.'
    return
  }

  isSaving.value = true

  try {
    const session = await getAuthToken()
    const idToken = session.tokens?.idToken?.toString()

    if (!idToken) {
      throw new Error('Your authentication session could not be found.')
    }

    const response = await fetch(updateProfileApiUrl, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${idToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        displayName: profile.displayName,
        artistWebsite: profile.artistWebsite,
        bio: profile.bio,
        avatarUrl: profile.avatarUrl,
        instagramHandle: normalizeInstagramHandle(profile.instagramHandle),
      }),
    })

    const responseBody = await response.json().catch(() => null)

    if (!response.ok) {
      throw new Error(responseBody?.message ?? 'Unable to update your profile.')
    }

    profile.instagramHandle = normalizeInstagramHandle(profile.instagramHandle)

    statusMessage.value = 'Your profile was updated successfully.'
  } catch (error) {
    hasError.value = true
    statusMessage.value = error instanceof Error ? error.message : 'Unable to update your profile.'
  } finally {
    isSaving.value = false
  }
}
</script>

<style scoped>
.profile-page {
  display: flex;
  justify-content: center;
  padding: 2rem 1rem;
}

.profile-card {
  width: 100%;
  max-width: 700px;
  padding: 2rem;
  background-color: white;
  border: 1px solid #d3d3d3;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgb(0 0 0 / 8%);
}

.profile-heading {
  margin-bottom: 2rem;
}

.profile-heading h1 {
  margin: 0 0 0.5rem;
}

.profile-heading p {
  margin: 0;
  color: #555;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  color: #222;
  background-color: white;
  border: 1px solid #aaa;
  border-radius: 4px;
  font: inherit;
  box-sizing: border-box;
}

.form-group textarea {
  resize: vertical;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: 3px solid #8ab4f8;
  outline-offset: 1px;
  border-color: #3f3f3f;
}

.instagram-input {
  display: flex;
  align-items: center;
  border: 1px solid #aaa;
  border-radius: 4px;
  overflow: hidden;
}

.instagram-input span {
  padding: 0.75rem 0 0.75rem 0.75rem;
  color: #555;
}

.instagram-input input {
  border: none;
}

.instagram-input:focus-within {
  outline: 3px solid #8ab4f8;
  outline-offset: 1px;
  border-color: #3f3f3f;
}

.instagram-input input:focus {
  outline: none;
}

.avatar-preview {
  width: 96px;
  height: 96px;
  margin-top: 0.5rem;
  object-fit: cover;
  border: 1px solid #ccc;
  border-radius: 50%;
}

.character-count {
  margin: 0;
  color: #666;
  font-size: 0.875rem;
  text-align: right;
}

.field-error,
.status-message.error {
  color: #a40000;
}

.field-error,
.status-message {
  margin: 0;
}

.status-message {
  padding: 0.75rem;
  background-color: #eef8ee;
  border-radius: 4px;
}

.status-message.error {
  background-color: #fff0f0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

.save-button {
  padding: 0.7rem 1.25rem;
  color: white;
  background-color: #3f3f3f;
  border: none;
  border-radius: 4px;
  font: inherit;
  cursor: pointer;
}

.save-button:hover:not(:disabled) {
  background-color: #292929;
}

.save-button:focus-visible {
  outline: 3px solid #8ab4f8;
  outline-offset: 2px;
}

.save-button:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}

@media (max-width: 640px) {
  .profile-page {
    padding: 1rem;
  }

  .profile-card {
    padding: 1.25rem;
  }

  .form-actions {
    justify-content: stretch;
  }

  .save-button {
    width: 100%;
  }
}
</style>

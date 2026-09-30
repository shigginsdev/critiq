<template>
  <p>{{ displayName ? `Welcome, ${displayName}!` : 'Welcome!' }}</p>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { getUserProfile } from '@/services/profile'

const props = defineProps<{ userId: string }>()
const displayName = ref('')

watch(
  () => props.userId,
  async (userId, _previousUserId, onCleanup) => {
    let active = true
    onCleanup(() => {
      active = false
    })
    displayName.value = ''
    if (!userId) return

    try {
      const profile = await getUserProfile()
      if (active) displayName.value = profile.displayName?.trim() ?? ''
    } catch (error) {
      if (active) console.error('Unable to load the welcome name:', error)
    }
  },
  { immediate: true },
)
</script>

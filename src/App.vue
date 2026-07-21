<template>
  <div class="app-container">
    <Authenticator>
      <template #default="{ user, signOut }">
        <header>
          <p>Welcome, {{ user.username }}!</p>
          <button @click="signOut">Sign Out</button>
        </header>

        <RouterView />
      </template>
    </Authenticator>
  </div>
</template>

<script setup lang="ts">
import { Authenticator } from '@aws-amplify/ui-vue'
import { RouterView } from 'vue-router'
import '@aws-amplify/ui-vue/styles.css'
</script>

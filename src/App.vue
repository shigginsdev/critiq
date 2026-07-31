<template>
  <div class="app-container">
    <Authenticator>
      <template #default="{ user, signOut }">
        <header class="app-header">
          <p class="welcome-message">Welcome, {{ user.username }}!</p>

          <div class="header-actions">
            <RouterLink class="header-button" to="/profile"> Profile </RouterLink>

            <button class="header-button" type="button" @click="signOut">Sign Out</button>
          </div>
        </header>

        <RouterView />
      </template>
    </Authenticator>
  </div>
</template>

<script setup lang="ts">
import { Authenticator } from '@aws-amplify/ui-vue'
import { RouterLink, RouterView } from 'vue-router'
import '@aws-amplify/ui-vue/styles.css'
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}

.app-header {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
}

.welcome-message {
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
  margin-left: auto;
}

.header-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.6rem 1rem;
  color: white;
  background-color: #3f3f3f;
  border: none;
  border-radius: 4px;
  font: inherit;
  line-height: 1.2;
  text-decoration: none;
  cursor: pointer;
}

.header-button:hover {
  background-color: #292929;
}

.header-button:focus-visible {
  outline: 3px solid #8ab4f8;
  outline-offset: 2px;
}
</style>

<template>
  <div class="app-container">
    <Authenticator>
      <template #default="{ user, signOut }">
        <header class="app-header">
          <p class="welcome-message">Welcome, {{ user.username }}!</p>

          <!-- Desktop navigation -->
          <nav class="desktop-actions" aria-label="Account navigation">
            <RouterLink class="header-button" to="/profile"> Profile </RouterLink>

            <button class="header-button" type="button" @click="signOut">Sign Out</button>
          </nav>

          <!-- Mobile hamburger button -->
          <button
            class="menu-toggle"
            type="button"
            aria-label="Toggle account menu"
            :aria-expanded="isMenuOpen"
            aria-controls="mobile-account-menu"
            @click="toggleMenu"
          >
            <svg class="menu-icon" viewBox="0 0 24 24" aria-hidden="true">
              <path v-if="!isMenuOpen" d="M4 6h16M4 12h16M4 18h16" />

              <path v-else d="M6 6l12 12M18 6L6 18" />
            </svg>
          </button>

          <!-- Mobile dropdown menu -->
          <nav
            v-if="isMenuOpen"
            id="mobile-account-menu"
            class="mobile-menu"
            aria-label="Account navigation"
          >
            <RouterLink class="mobile-menu-item" to="/profile" @click="closeMenu">
              Profile
            </RouterLink>

            <button class="mobile-menu-item" type="button" @click="handleSignOut(signOut)">
              Sign Out
            </button>
          </nav>
        </header>

        <RouterView />
      </template>
    </Authenticator>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Authenticator } from '@aws-amplify/ui-vue'
import { RouterLink, RouterView } from 'vue-router'
import '@aws-amplify/ui-vue/styles.css'

const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

const handleSignOut = (signOut: () => void) => {
  closeMenu()
  signOut()
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}

.app-header {
  position: relative;
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
}

.welcome-message {
  margin: 0;
}

.desktop-actions {
  display: flex;
  gap: 0.75rem;
  margin-left: auto;
}

.header-button,
.mobile-menu-item {
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

.header-button:hover,
.mobile-menu-item:hover {
  background-color: #292929;
}

.header-button:focus-visible,
.mobile-menu-item:focus-visible,
.menu-toggle:focus-visible {
  outline: 3px solid #8ab4f8;
  outline-offset: 2px;
}

/* Hidden on desktop */
.menu-toggle,
.mobile-menu {
  display: none;
}

@media (max-width: 640px) {
  .app-header {
    padding: 1rem;
  }

  .welcome-message {
    max-width: calc(100% - 60px);
    overflow-wrap: anywhere;
  }

  .desktop-actions {
    display: none;
  }

  .menu-toggle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    margin-left: auto;
    padding: 0;
    color: white;
    background-color: #3f3f3f;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .menu-toggle:hover {
    background-color: #292929;
  }

  .menu-icon {
    width: 26px;
    height: 26px;
    fill: none;
    stroke: currentColor;
    stroke-width: 2;
    stroke-linecap: round;
  }

  .mobile-menu {
    position: absolute;
    top: calc(100% - 0.25rem);
    right: 1rem;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    width: 160px;
    padding: 0.5rem;
    background-color: white;
    border: 1px solid #d3d3d3;
    border-radius: 6px;
    box-shadow: 0 4px 12px rgb(0 0 0 / 18%);
  }

  .mobile-menu-item {
    width: 100%;
    margin: 0;
  }

  .mobile-menu-item + .mobile-menu-item {
    margin-top: 0.5rem;
  }
}
</style>

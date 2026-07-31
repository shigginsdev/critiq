<template>
  <main class="profile-page">
    <section class="profile-card">
      <h1>Profile</h1>

      <p>Your profile information will appear here.</p>
    </section>
  </main>
</template>

<script setup lang="ts">
// Profile functionality will be added here.
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

.profile-card h1 {
  margin-top: 0;
  margin-bottom: 1rem;
}

.profile-card p {
  margin-bottom: 0;
}
</style>

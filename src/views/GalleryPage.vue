<template>
  <main class="gallery-page">
    <header class="gallery-header">
      <h1>Critique Gallery</h1>
      <p>Development placeholder gallery</p>
    </header>

    <section class="gallery-grid">
      <article v-for="artwork in artworks" :key="artwork.id" class="gallery-card">
        <img :src="artwork.imageUrl" :alt="artwork.title" class="gallery-image" />

        <div class="gallery-info">
          <h2>{{ artwork.title }}</h2>
          <p>{{ artwork.date }}</p>
        </div>
      </article>
    </section>
  </main>
</template>

<script setup>
defineOptions({
  name: 'GalleryPage',
})

const placeholderImage =
  'https://images.unsplash.com/photo-1603979649806-5299879db16b?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'

const artworks = [
  { id: 1, title: 'Mountain Study', date: 'Apr 2026', imageUrl: placeholderImage },
  { id: 2, title: 'Still Life Pears', date: 'Apr 2026', imageUrl: placeholderImage },
  { id: 3, title: 'Quiet Barn', date: 'Mar 2026', imageUrl: placeholderImage },
  { id: 4, title: 'Rooster Sketch', date: 'Mar 2026', imageUrl: placeholderImage },
  { id: 5, title: 'Blue Vase', date: 'Feb 2026', imageUrl: placeholderImage },
  { id: 6, title: 'Evening Field', date: 'Feb 2026', imageUrl: placeholderImage },
  { id: 7, title: 'Goat Portrait', date: 'Jan 2026', imageUrl: placeholderImage },
  { id: 8, title: 'Charcoal Hare', date: 'Jan 2026', imageUrl: placeholderImage },
  { id: 9, title: 'Window Light', date: 'Dec 2025', imageUrl: placeholderImage },
  { id: 10, title: 'Aspen Path', date: 'Dec 2025', imageUrl: placeholderImage },
  { id: 11, title: 'Clay Pot Study', date: 'Nov 2025', imageUrl: placeholderImage },
  { id: 12, title: 'Western Sky', date: 'Nov 2025', imageUrl: placeholderImage },
]
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

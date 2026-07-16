import { createRouter, createWebHistory } from 'vue-router'
import GalleryPage from '../views/GalleryPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/app',
    },
    {
      path: '/gallery',
      component: GalleryPage,
    },
  ],
})

export default router

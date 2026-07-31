import { createRouter, createWebHistory } from 'vue-router'
import GalleryPage from '../views/GalleryPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/gallery',
    },
    {
      path: '/gallery',
      component: GalleryPage,
    },
    {
      path: '/profile',
      component: () => import('../views/ProfilePage.vue'),
    },
  ],
})

export default router

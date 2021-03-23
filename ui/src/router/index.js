import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: () => import('../components/Landing.vue'),
  },
  {
    path: '/auth/callback',
    name: 'Callback',
    component: () => import('../components/Callback.vue'),
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../components/Home.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;

import Vue from 'vue'
import VueRouter from 'vue-router'

import Acoes from '@/views/Acoes'
import Home from '@/views/Home'
import Setores from '@/views/Setores'
import Carteiras from '@/views/Carteiras'

Vue.use(VueRouter)

const routes = [
  {
    name: 'Home',
    path: '/',
    component: Home
  },
  {
    name: 'Acoes',
    path: '/acoes',
    component: Acoes
  },
  {
    name: 'Setores',
    path: '/setores',
    component: Setores
  },
  {
    name: 'Carteiras',
    path: '/carteiras',
    component: Carteiras
  } ,
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

export default new VueRouter({
  mode: 'history',
  routes
})


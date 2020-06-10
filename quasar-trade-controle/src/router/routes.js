
const routes = [
  {
    path: '/', redirect: 'dashboard'
  },
  {
    name: 'Dashboard',
    path: '/dashboard',
    component: () => import('pages/Index.vue')
  },
  {
    name: 'Carteiras',
    path: '/carteiras',
    component: () => import('pages/carteira/Carteiras.vue')
  },
  {
    name: 'Acoes',
    path: '/acoes',
    component: () => import('pages/Acoes.vue')
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes

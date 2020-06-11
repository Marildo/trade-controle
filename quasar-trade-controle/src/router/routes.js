
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
    path: '/carteiras',
    component: () => import('pages/carteira/Carteiras.vue'),
    children: [
      { name: 'Carteiras', path: '', component: () => import('pages/carteira/Index.vue') },
      { name: 'Carteira', path: ':id', component: () => import('pages/carteira/Carteira.vue'), props: true }
    ]
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

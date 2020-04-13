import Vue from 'vue'
import Router from 'vue-router'
import Acoes from '@/components/pages/Acoes'
import Home from '@/components/pages/Home'
import Setores from '@/components/pages/Setores'
import Carteiras from '@/components/pages/Carteiras'

Vue.use(Router)

export default new Router({
    mode:'history',
    routes: [
        {  
            path: '/',
            component: Home
        },
        {
            path:'/acoes',
            component:Acoes
        },
        {
            path:'/setores',
            component:Setores
        },
        {
            path:'/carteiras',
            component:Carteiras
        }
    ]
})
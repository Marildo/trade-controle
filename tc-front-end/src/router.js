import Vue from 'vue'
import Router from 'vue-router'
import Acoes from '@/views/Acoes'
import Home from '@/views/Home'
import Setores from '@/views/Setores'
import Carteiras from '@/views/Carteiras'

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
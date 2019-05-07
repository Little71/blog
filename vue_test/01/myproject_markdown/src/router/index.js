import Vue from 'vue'
import Router from 'vue-router'
import Vmain from '@/components/Vmain'
import Vnote from '@/components/Vnote'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'main',
      component: Vmain
    },
    {
      path:'/note',
      name:'note',
      component:Vnote
    }
  ]
})

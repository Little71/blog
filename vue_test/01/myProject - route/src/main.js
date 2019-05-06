import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'

// 1. 定义 (路由) 组件。
// 可以从其他文件 import 进来
import Vmain from './components/Vmain'
import Vcourse from './components/Vcourse'
import Vmarked from './components/Vmarked'

Vue.use(VueRouter)

// 2. 定义路由
// 每个路由应该映射一个组件。 其中"component" 可以是
// 通过 Vue.extend() 创建的组件构造器，
// 或者，只是一个组件配置对象。
// 我们晚点再讨论嵌套路由。
const routes = [
  { path: '/', component: Vmain },
  { path: '/course', component: Vcourse },
  { path: '/marked', component: Vmarked },
]

// 3. 创建 router 实例，然后传 `routes` 配置
// 你还可以传别的配置参数,
// 或者直接传入一个数组
const router = new VueRouter({
  mode: 'history',
  routes // (缩写) 相当于 routes: routes
})

// const router = new VueRouter({
//   routes:[
//     { path: '/', component: Vmain },
//     { path: '/course', component: Vcourse },
//     { path: '/marked', component: Vmarked },
//   ]
// })

new Vue({
  el: '#app',
  router, //等价于 router:router
  render: h => h(App)
})

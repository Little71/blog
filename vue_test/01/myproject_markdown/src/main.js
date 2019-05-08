// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuex from 'vuex'
import $ from 'jquery';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios';

Vue.use(ElementUI);

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    //这里面的状态跟组件的数据属性有关系
    alllist: [],
    note: {
      title: '',
      content: '',
      markdown: '',
    }
  },
  mutations: {
    GETALLDATAS(state, newdata) {
      state.alllist = newdata;
    },
    ADDONENOTE(state, newdata) {
      state.alllist = newdata;
    },
    DELETENOTE(state, newdata) {
      state.alllist = newdata;
    }
  },
  actions: {
    getAllDatas(state) {
      $.ajax({
        url: '',
        methods: 'get',
        success: function (data) {
          state.alllist = data;
        }
      });
      // axios.get('url').then(function (response) { 
      //   console.log(response);
      // }).catch(function (error) { 
      //   console.log(error);
      // });
    },
    addOneNote(context, json) {
      $.ajax({
        url: "",
        methods: "post",
        data: json,
        success: function (data) {
          context.commit('ADDONENOTE', data);
        },
        error: function (error) { }
      });
      axios.post('url',{}).then(function(response){
        console.log(response);
      }).catch(function(errpr){
        console.log(errpr);
      });
      axios.interceptors.request.use
    },
    deleteNote(context, id) {
      $.ajax({
        url: "",
        methods: "delete",
        data: id,
        success: function (data) {
          context.commit('DELETENOTE', data);
        },
        error: function (error) { }
      });
    },
  }
})


Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})

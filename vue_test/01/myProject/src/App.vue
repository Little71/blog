<template>
  <div id="app">
    <Vheader></Vheader>
    <img :src="imgStr">
    <h1>{{ msg }}</h1>

    <!-- 自定义事件 -->
    <Vcontent @addZhuangHandler="addHandler(str)"></Vcontent>
    
    <!-- 给子组件绑定自定义属性 -->
    <Vfooter v-bind:cityArray="city"></Vfooter>
  </div>
</template>

<script>
import Vheader from "./components/Vheader";
import Vcontent from "./components/Vcontent";
import Vfooter from "./components/Vfooter";

//导入 相当于把一个组件资源赋值给一个变量
import imgStr from "./assets/logo.png";

export default {
  name: "app",
  imgStr: imgStr,
  data() {
    return {
      msg: "hello world",
      city: ["北", "上", "广"]
    };
  },
  methods: {
    addHandler(str){
      this.city.push(str);
    }
  },
  computed: {},
  components: {
    Vheader,
    Vcontent,
    Vfooter
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
}
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1,
h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
  color: red;
  text-decoration: none;
}
</style>

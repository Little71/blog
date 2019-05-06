<template>
  <div id="app">
    <img src="./assets/logo.png">
    <h1>{{ msg }}</h1>

    <Vheader></Vheader>
    <Vcontent></Vcontent>
    <Vfooter></Vfooter>
  </div>
</template>

<script>
import Vheader from './components/Vheader.vue';
import Vcontent from './components/Vcontent.vue';
import Vfooter from './components/Vfooter.vue';

export default {
  name: 'app',
  data () {
    return {
      msg: 'hello world'
    }
  },
  methods:{},
  computed:{},
  components:{
    Vheader,
    Vcontent,
    Vfooter,
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1, h2 {
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

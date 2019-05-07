<template>
  <div id="app">
    <Vheader></Vheader>
    <router-view/>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.min.css';
import Vheader from './components/Vheader';
import $ from 'jquery';

export default {
  name: 'App',
  data(){
    return {
    }
  },
  components:{
    Vheader,
  },
  //页面结构加载完成了就会执行
  mounted(){
    var _this=this;
    $.ajax({
      url:'',
      methods:'get',
      success:function(data){
        _this.$store.state.alllist = data;
      }
    });
  }
}
</script>

<style>

</style>

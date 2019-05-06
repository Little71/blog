<template>
  <footer class="foot">
    
    <ul v-for='item in cityArray'>
      {{item}}
    </ul>
  </footer>
</template>
<script>
export default {
  name: "Vfooter",
  data() {
    return {};
  },
  props:{
    //接收父组件传递的数据，要根据数据的类型做校验，如下是数组类型
    cityArray:Array,
  }
};
</script>
<style>
</style>

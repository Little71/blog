<template>
  <button class="btn" :class="currentBtn">
    <!-- 插槽 进行分发 -->
    <slot>按钮</slot>
  </button>
</template>

<script>
export default {
  name: "VnoteBtn",
  data() {
    return {};
  },
  props: {
    typed: String,
  },
  computed:{
    currentBtn(){
      return {
        "btn-sucess":this.typed=="success"?true:false,
      }
    }
  }
};
</script>

<style scoped>
</style>


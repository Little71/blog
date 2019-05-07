<template>
  <li>
    <h2>{{date.title}}</h2>
    <p>{{date.content}}</p>
    <!-- <el-button type="danger" icon="el-icon-delete" circle></el-button> -->
    <VnoteBtn typed = "danger" @click='deletehandler'>删除按钮</VnoteBtn>
  </li>
</template>

<script>
import VnoteBtn from './VnoteBtn';
export default {
  name: "VnoteItem",
  data() {
    return {};
  },
  props: {
    data: Object,
  },
  components:{
    VnoteBtn
  },
  methods:{
    deletehandler(){
      this.$store.dispatch('deleteNote',this.data.id)
    }
  }
};
</script>

<style scoped>
</style>


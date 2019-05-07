<template>
  <ul>
    <VnoteItem v-for="(item,index) in getAllDates" :date='item'></VnoteItem>
  </ul>
</template>

<script>
import VnoteItem from "./VnoteItem";
export default {
  name: "VnoteList",
  data() {
    return {};
  },
  components: {
    VnoteItem
  },
  computed: {
    getAllDates() {
      return this.$store.state.alllist;
    }
  }
};
</script>

<style scoped>
</style>


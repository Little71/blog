<template>
  <li>
    <h2>{{date.title}}</h2>
    <p>{{date.content}}</p>
  </li>
</template>

<script>
export default {
  name: "VnoteItem",
  data() {
    return {};
  },
  props: {
    data: Object,
  }
};
</script>

<style scoped>
</style>


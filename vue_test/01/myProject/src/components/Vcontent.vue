<template>
  <div class="wrap">
    <div class="t">
      <button @click="addCunhandler">添加一个村</button>
    </div>
    <div class="mark">
      <textarea class="editor" name id cols="100" rows="10" v-model="markValue"></textarea>
      <div class="show" v-html="currentValue"></div>
    </div>
  </div>
</template>
<script>
import Marked from "marked";
export default {
  name: "Vcontent",
  data() {
    return {
      markValue: ""
    };
  },
  methods: {
    addCunhandler() {
      //触发自定义事件，传入自定义事件名字
      this.$emit("addZhuangHandler", "石景山");
      //相当于 addZhuangHandler(石景山) 把第二个参数作为第一个参数的函数的参数
    }
  },
  computed: {
    currentValue() {
      return Marked(this.markValue);
    }
  }
};
</script>
<style>
.t {
  width: 300px;
  height: 100px;
}
.mark {
  width: 1210px;
  height: 600px;
  margin: 0 auto;
}

.editor,
.show {
  float: left;
  width: 603px;
  height: 600px;
  border: 1px solid #666;
}
</style>

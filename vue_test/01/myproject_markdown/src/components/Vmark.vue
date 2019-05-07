<template>
  <div class="wrap">
    请输入文章标题：
    <input type="text" v-model="titlehandler">
    <button class="btn btn-success" @click="addOneNote">提交</button>
    <div class="mark">
      <textarea class="editor" name id cols="100" rows="10" v-model="markdownHandler"></textarea>
      <div class="show" v-html="currentValue" ref="t"></div>
    </div>
  </div>
</template>
<script>
import Marked from "marked";
import $ from "jquery";

export default {
  name: "Vmark",
  data() {
    return {
      markValue: "",
      title: ""
    };
  },
  methods: {
    addOneNote() {
      var json = {
        title: this.titlehandler,
        markdown: this.markdownHandler,
        content: this.$refs.t.innerText
        //获取有ref属性且值为t的标签
      };
      // 触发mutations的方法，有局限性只能用于同步操作
      // this.$store.commit("addOneNote", json);

      // 触发actions的方法，异步操作
      this.$store.dispatch("addOneNote", json);
    }
  },
  computed: {
    titlehandler: {
      set: function(newvalue) {
        this.$store.state.note.title = newvalue;
      },
      get: function() {
        return this.title;
      }
    },
    markdownHandler: {
      set: function(newvalue) {
        this.$store.state.note.markdown = newvalue;
      },
      get: function() {
        return this.markdown;
      }
    },
    currentValue() {
      return Marked(this.markdownHandler);
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
  width: 800px;
  height: 400px;
  margin: 0 auto;
}

.editor,
.show {
  float: left;
  width: 395px;
  height: 400px;
  border: 1px solid #666;
}
</style>

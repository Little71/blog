<template>
  <div class="container">
    <div class="row">
      <div class="col-md-3">
        <div class="panel panel-default">
          <div class="panel-heading">
            <h3 class="panel-title">笔记列表</h3>
          </div>
          <div class="panel-body">
            <!-- 笔记列表 -->
            <Vnoteshow></Vnoteshow>
          </div>
        </div>
      </div>
      <div class="col-md-9">
        <!-- markdown编辑器 -->
        <div class="panel panel-default">
          <div class="panel-heading">
            
          </div>
          <div class="panel-body">
               <Vmark></Vmark>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Vmark from "./Vmark";
import Vnoteshow from "./VnoteShow";
export default {
  name: "Vnote",
  data() {
    return {
        notelist:[
            {id:1,title:'tom',content:'嘻嘻嘻嘻嘻嘻'},
            {id:2,title:'jerry',content:'哈哈哈哈哈'},
            {id:3,title:'alex',content:'呵呵呵呵呵呵'},
        ]
    };
  },
  components: {
    Vmark,
    Vnoteshow
  }
};
</script>

<style scoped>
</style>


<template>
  <header class="header">
    <div class="nav">
      <div class="log">
        <img :src="imgStr" alt>
      </div>
      <div class="info">
        <button>注册</button><button>登录</button>
      </div>
    </div>
  </header>

</template>

<script>
import imgStr from "../assets/logo.png";
export default {
  name: "Vheader",
  data() {
    return {
      imgStr:imgStr,
    };
  }
};
</script>

<style scoped>
.header {
  width: 100%;
  height: 40px;
  background-color: #fff;
  box-shadow: 0 2px 4px 0 #c9c9c9;
}
.header .nav {
  width: 980px;
  height: 40px;
  margin: 0 auto;
}
.nav .logo {
  width: 100px;
  height: 40px;
  float: left;
}
.logo img{
  width: 40px;
  height: 40px;
}
.nav .info{
  float: right;
  width: 200px;
  height: 40px;
}
.info button{
  width: 80px;
  height: 40px;
  float:left;
}
</style>

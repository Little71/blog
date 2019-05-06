<template>
  <div id="app">
    <p>
      <!-- 使用 router-link 组件来导航. -->
      <!-- 通过传入 `to` 属性指定链接，即渲染成href. -->
      <!-- <router-link> 默认会被渲染成一个 `<a>` 标签 -->
      <router-link to="/">main</router-link>
      <router-link to="/course">course</router-link>
      <router-link to="/marked">marked</router-link>
    </p>
    <!-- 路由出口 -->
    <!-- 路由匹配到的组件将渲染在这里 -->
    <router-view></router-view>
  </div>
</template>

<script>
import "bootstrap/dist/css/bootstrap.min.css";
export default {
  name: "app",
  data() {
    return {};
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
}
</style>

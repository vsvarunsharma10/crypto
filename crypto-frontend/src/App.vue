<template>
    <v-app id="app">
      <v-content class="mx-4 mb-4">
        <router-view app></router-view>
      </v-content>
    </v-app>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  /* font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px; */
}
</style>

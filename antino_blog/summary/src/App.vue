<template>
  <nav>
    <router-link style="margin-left: 5px; margin-right: 5px;" to="/monthly_report">Monthly Summary</router-link>
    <router-link style="margin-left: 5px; margin-right: 5px;" to="/weekly_report">Weekly Summary</router-link>
    <router-link style="margin-left: 5px; margin-right: 5px;" to="/quarterly_report">Quaterly Summary</router-link>
    <router-link style="margin-left: 5px; margin-right: 5px;" to="/yearly_report">Yearly Summary</router-link>
  </nav>
  <router-view/>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>

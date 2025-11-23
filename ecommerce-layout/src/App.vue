<template>
  <HeaderBar />
  <MarqueeBar />
  <HeaderMain />
  <ProductCard />
</template>

<script>
import HeaderBar from './components/HeaderBar.vue'
import MarqueeBar from './components/MarqueeBar.vue'
import HeaderMain from './components/HeaderMain.vue'
import ProductCard from './components/ProductCard.vue'

export default {
  name: 'App',
  components: {
    HeaderBar,
    MarqueeBar,
    HeaderMain,
    ProductCard
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

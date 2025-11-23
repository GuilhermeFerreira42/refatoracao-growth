<template>
  <div class="product-showcase">
    <!-- Vitrine de produtos da parte_10.html -->
    <ProductCard v-for="n in 4" :key="n" />
  </div>
</template>

<script>
import ProductCard from './ProductCard.vue'
export default {
  name: 'ProductShowcase',
  components: { ProductCard }
}
</script>

<style scoped>
.product-showcase {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
}
</style>

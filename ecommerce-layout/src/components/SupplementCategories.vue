<template>
  <div class="supplement-categories">
    <!-- Categorias de suplemento da parte_10.html -->
    <div class="category" v-for="cat in categories" :key="cat.name">
      <img :src="cat.img" :alt="cat.name" class="category-img" />
      <span class="category-label">{{ cat.name }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SupplementCategories',
  data() {
    return {
      categories: [
        { name: 'Proteínas', img: '/assets/cat-proteinas.jpg' },
        { name: 'Aminoácidos', img: '/assets/cat-aminoacidos.jpg' },
        { name: 'Vitaminas', img: '/assets/cat-vitaminas.jpg' },
        { name: 'Termogênicos', img: '/assets/cat-termogenicos.jpg' }
      ]
    }
  }
}
</script>

<style scoped>
.supplement-categories {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
}
.category {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.category-img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(44,62,80,0.10);
  margin-bottom: 0.5rem;
}
.category-label {
  color: #0056b3;
  font-weight: bold;
  font-size: 1rem;
}
</style>

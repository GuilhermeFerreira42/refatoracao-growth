<template>
  <div class="main-banner">
    <!-- Banner principal da parte_10.html -->
    <img src="/assets/banner-principal.jpg" alt="Banner Principal" class="banner-img" />
  </div>
</template>

<script>
export default {
  name: 'MainBanner'
}
</script>

<style scoped>
.main-banner {
  width: 100%;
  margin-bottom: 2rem;
}
.banner-img {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(44,62,80,0.12);
}
</style>

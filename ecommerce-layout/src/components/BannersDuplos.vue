<template>
  <section class="bannersDuplos">
    <div class="bannersDuplos-container flex-container">
      <div class="banner-duplo-item">
        <img src="https://via.placeholder.com/600x300/1899d5/fff?text=Banner+Duplo+1" alt="Banner Duplo 1" />
      </div>
      <div class="banner-duplo-item">
        <img src="https://via.placeholder.com/600x300/001d45/fff?text=Banner+Duplo+2" alt="Banner Duplo 2" />
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'BannersDuplos'
}
</script>

<style scoped>
.bannersDuplos {
  margin-top: 20px;
}
.bannersDuplos-container {
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  gap: 16px;
  justify-content: center;
}
.banner-duplo-item {
  flex: 1;
  min-width: 280px;
  max-width: 600px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 10px rgba(0,0,0,.08);
}
.banner-duplo-item img {
  width: 100%;
  display: block;
  border-radius: 8px;
}
@media (max-width: 1023px) {
  .bannersDuplos-container {
    flex-direction: column;
    gap: 8px;
  }
  .banner-duplo-item {
    max-width: 100%;
  }
}
</style>

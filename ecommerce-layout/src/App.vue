<template>
  <div id="mainContainerSite">
    <HeaderBar />
    <MarqueeBar />
    <HeaderMain />
    <div class="menuBarWeContainer">
      <MenuBar />
    </div>
    <main class="mainHomeContainer">
      <div class="weContainer">
        <MainBanner />
        <PitchBar />
        <SupplementCategories />
        <WheyBanner />
        <ProductShowcase />
        <Depoimentos />
        <BannersDuplos />
        <BannersEsportes />
        <div class="product-list">
          <ProductCard v-for="n in 18" :key="n" />
        </div>
      </div>
    </main>
    <FooterBar />
  </div>
</template>

<script>
import HeaderBar from './components/HeaderBar.vue'
import MarqueeBar from './components/MarqueeBar.vue'
import HeaderMain from './components/HeaderMain.vue'
import MenuBar from './components/MenuBar.vue'
import ProductCard from './components/ProductCard.vue'
import MainBanner from './components/MainBanner.vue'
import PitchBar from './components/PitchBar.vue'
import SupplementCategories from './components/SupplementCategories.vue'
import WheyBanner from './components/WheyBanner.vue'
import ProductShowcase from './components/ProductShowcase.vue'
import Depoimentos from './components/Depoimentos.vue'
import FooterBar from './components/FooterBar.vue'
import BannersDuplos from './components/BannersDuplos.vue'

export default {
  name: 'App',
  components: {
    HeaderBar,
    MarqueeBar,
    HeaderMain,
    MenuBar,
    ProductCard,
    MainBanner,
    PitchBar,
    SupplementCategories,
    WheyBanner,
    ProductShowcase,
    Depoimentos,
    FooterBar,
    BannersDuplos
  }
}
</script>

<style>
#mainContainerSite {
  display: flex;
  flex-direction: column;
  width: 100%;
}
.mainHomeContainer {
  background: #f6f8fa;
  width: 100%;
  flex: 1;
}
.weContainer {
  max-width: 1670px;
  margin: 0 auto;
  padding: 0 5px;
  width: 100%;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-gap: 15px;
}
.weContainer > * {
  grid-column: 1 / 13;
}
@media (max-width: 1023px) {
  .weContainer {
    padding: 0 15px;
    grid-gap: 8px;
  }
}
.product-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
}
</style>

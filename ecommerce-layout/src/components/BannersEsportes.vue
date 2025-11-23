<template>
  <section class="bannersEsporte">
    <div class="weContainer-deskAutoCol8">
      <div class="bannersEsporte-container">
        <img src="https://via.placeholder.com/600x300/1899d5/fff?text=Banner+Esporte+1" alt="Banner Esporte 1" />
        <div class="bannersEsporte-item-t1">Musculação</div>
      </div>
      <div class="bannersEsporte-container">
        <img src="https://via.placeholder.com/600x300/001d45/fff?text=Banner+Esporte+2" alt="Banner Esporte 2" />
        <div class="bannersEsporte-item-t1">Crossfit</div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'BannersEsportes'
}
</script>

<style scoped>
.bannersEsporte {
  margin-top: 47px;
}
.weContainer-deskAutoCol8 {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 21px;
}
.bannersEsporte-container {
  border-radius: 10px;
  overflow: hidden;
  position: relative;
  width: calc(50% - 8px);
  box-shadow: 0 1px 10px rgba(0,0,0,.08);
}
.bannersEsporte-container img {
  width: 100%;
  display: block;
  border-radius: 10px;
}
.bannersEsporte-item-t1 {
  position: absolute;
  bottom: 17px;
  left: 23px;
  color: #fff;
  font-weight: 700;
  font-size: 30px;
  line-height: 34px;
  text-shadow: 0 2px 8px rgba(0,0,0,.3);
}
@media (max-width: 1023px) {
  .weContainer-deskAutoCol8 {
    flex-direction: column;
    gap: 8px;
    max-width: 414px;
    margin: 0 auto;
  }
  .bannersEsporte-container {
    width: 100%;
    margin-bottom: 8px;
  }
  .bannersEsporte-item-t1 {
    font-size: 18px;
    left: 10px;
    bottom: 10px;
  }
}
</style>

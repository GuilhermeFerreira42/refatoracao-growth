<template>
  <section class="depoimentosHome">
    <div class="depoimentosHome-boxLogo">
      <img src="/src/assets/logo.png" alt="Logo Growth" />
      <div class="depoimentosHome-boxLogo-text">
        <div class="depoimentosHome-boxLogo-text-t1">O que dizem sobre a Growth</div>
        <div class="depoimentosHome-boxLogo-text-t2">Depoimentos de clientes reais</div>
      </div>
    </div>
    <div class="depoimentosHome-carrossel">
      <!-- Carrossel de depoimentos (mock) -->
      <div class="depoimento-item">
        <blockquote>Produtos excelentes, entrega rápida e preço justo!</blockquote>
        <span class="depoimento-autor">João S.</span>
      </div>
      <div class="depoimento-item">
        <blockquote>Atendimento impecável, recomendo a todos!</blockquote>
        <span class="depoimento-autor">Maria F.</span>
      </div>
      <div class="depoimento-item">
        <blockquote>Qualidade garantida, compro sempre!</blockquote>
        <span class="depoimento-autor">Carlos M.</span>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'DepoimentosSection'
}
</script>

<style scoped>
.depoimentosHome {
  align-items: center;
  background: linear-gradient(90deg, #1899d5 0%, #001d45 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 60px 0 30px 0;
  margin: 40px 0;
  border-radius: 16px;
}
.depoimentosHome-boxLogo {
  display: flex;
  align-items: center;
  margin-bottom: 42px;
}
.depoimentosHome-boxLogo img {
  max-width: 132px;
}
.depoimentosHome-boxLogo-text {
  margin-left: 40px;
}
.depoimentosHome-boxLogo-text-t1 {
  font-size: 34px;
  font-weight: 700;
}
.depoimentosHome-boxLogo-text-t2 {
  font-size: 20px;
  margin-top: 17px;
}
.depoimentosHome-carrossel {
  display: flex;
  gap: 32px;
  justify-content: center;
}
.depoimento-item {
  background: #fff;
  color: #1899d5;
  border-radius: 8px;
  padding: 24px;
  min-width: 260px;
  box-shadow: 0 3px 16px rgba(0,0,0,.12);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.depoimento-item blockquote {
  font-size: 1.1rem;
  font-style: italic;
  margin-bottom: 12px;
}
.depoimento-autor {
  font-weight: 700;
  font-size: 1rem;
}
@media (max-width: 1023px) {
  .depoimentosHome {
    padding: 30px 0 10px 0;
    margin: 20px 0;
  }
  .depoimentosHome-boxLogo {
    flex-direction: column;
    text-align: center;
  }
  .depoimentosHome-boxLogo-text {
    margin-left: 0;
    margin-top: 25px;
  }
  .depoimentosHome-boxLogo-text-t1 {
    font-size: 20px;
  }
  .depoimentosHome-boxLogo-text-t2 {
    font-size: 16px;
    margin-top: 10px;
  }
  .depoimentosHome-carrossel {
    flex-direction: column;
    gap: 16px;
    align-items: center;
  }
  .depoimento-item {
    min-width: 180px;
    padding: 16px;
  }
}
</style>

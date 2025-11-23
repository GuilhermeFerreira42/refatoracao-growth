<template>
  <section class="pitchbar">
    <div class="pitchbar-container">
      <div class="pitchbar-item">
        <div class="pitchbar-item-icone">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="16" fill="#fff"/><path d="M8 20l8-8 8 8" stroke="#1899d5" stroke-width="2" fill="none"/></svg>
        </div>
        <div class="pitchbar-item-text">
          <span class="pitchbar-item-text-t1">Frete grátis</span>
          <span class="pitchbar-item-text-t2">acima de R$250</span>
        </div>
      </div>
      <div class="pitchbar-item">
        <div class="pitchbar-item-icone">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="16" fill="#fff"/><text x="8" y="22" font-size="14" fill="#1899d5" font-weight="bold">10%</text></svg>
        </div>
        <div class="pitchbar-item-text">
          <span class="pitchbar-item-text-t1">10% OFF</span>
          <span class="pitchbar-item-text-t2">no PIX ou boleto</span>
        </div>
      </div>
      <div class="pitchbar-item">
        <div class="pitchbar-item-icone">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="16" fill="#fff"/><text x="7" y="22" font-size="14" fill="#1899d5" font-weight="bold">6x</text></svg>
        </div>
        <div class="pitchbar-item-text">
          <span class="pitchbar-item-text-t1">6x sem juros</span>
          <span class="pitchbar-item-text-t2">no cartão</span>
        </div>
      </div>
      <div class="pitchbar-item">
        <div class="pitchbar-item-icone">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="16" fill="#fff"/><path d="M10 22l6-12 6 12" stroke="#1899d5" stroke-width="2" fill="none"/></svg>
        </div>
        <div class="pitchbar-item-text">
          <span class="pitchbar-item-text-t1">Produtos Originais</span>
          <span class="pitchbar-item-text-t2">direto da fábrica</span>
        </div>
      </div>
      <div class="pitchbar-item">
        <div class="pitchbar-item-icone">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="16" fill="#fff"/><path d="M16 10v12M10 16h12" stroke="#1899d5" stroke-width="2"/></svg>
        </div>
        <div class="pitchbar-item-text">
          <span class="pitchbar-item-text-t1">Atendimento</span>
          <span class="pitchbar-item-text-t2">especializado</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'PitchBar'
}
</script>

<style scoped>
.pitchbar {
  margin-top: 45px;
}
.pitchbar-container {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 15px;
  background: #fff;
  border-radius: 45px;
  box-shadow: 0 1px 10px rgba(0,0,0,.08);
  padding: 20px 0;
}
.pitchbar-item {
  display: flex;
  align-items: center;
  background: #fff;
  border: 1px solid #dfdfdf;
  border-radius: 45px;
  padding-right: 20px;
}
.pitchbar-item-icone {
  background: #009edf;
  border-radius: 100%;
  width: 66px;
  height: 66px;
  margin-right: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.pitchbar-item-text-t1 {
  font-weight: 700;
  color: #1899d5;
}
.pitchbar-item-text-t2 {
  display: block;
  text-decoration: underline;
  color: #000;
}
@media (max-width: 1023px) {
  .pitchbar-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
    border-radius: 16px;
    padding: 10px 0;
  }
  .pitchbar-item {
    flex-direction: column;
    align-items: flex-start;
    padding: 10px;
    border-radius: 16px;
  }
  .pitchbar-item-icone {
    width: 40px;
    height: 40px;
    margin-bottom: 5px;
  }
}
</style>

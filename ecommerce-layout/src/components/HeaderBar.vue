<template>
  <header class="header-bar">
    <div class="progress-bar__container">
      <div class="progress-bar_wrapper">
        <div class="progress-bar bar-effect">
          <div aria-live="polite" class="progress-bar__text-container">
            <div id="lottie-animation">
              <!-- SVG animado omitido para simplificação, pode ser inserido posteriormente -->
            </div>
            <p class="white">
              Adicione <b>R$&nbsp;250,00</b> ao carrinho para ter <b>FRETE GRÁTIS</b>
            </p>
          </div>
          <div role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" class="progress-bar-fill" style="width:0%;background-color:rgb(24,153,213)"></div>
        </div>
        <div class="progress-bar__select-container">
          <select id="state" name="state" aria-label="Selecione o estado">
            <option value="ac">Acre</option>
            <option value="al">Alagoas</option>
            <option value="ap">Amapá</option>
            <option value="am">Amazonas</option>
            <option value="ba">Bahia</option>
            <option value="ce">Ceará</option>
            <option value="df">Distrito Federal</option>
            <option value="es">Espírito Santo</option>
            <option value="go">Goiás</option>
            <option value="ma">Maranhão</option>
            <option value="mt">Mato Grosso</option>
            <option value="ms">Mato Grosso do Sul</option>
            <!-- ...demais estados... -->
          </select>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderBar',
};
</script>

<style scoped>
/* Estilos básicos para a barra de progresso e seletor de estado, mantendo o visual azul original */
.header-bar {
  background: #1899d5;
  padding: 0.5rem 0;
  color: #fff;
  font-size: 1rem;
}
.progress-bar__container {
  display: flex;
  justify-content: center;
  align-items: center;
}
.progress-bar_wrapper {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 1200px;
}
.progress-bar {
  flex: 1;
  display: flex;
  align-items: center;
  background: #1899d5;
  border-radius: 4px;
  margin-right: 1rem;
}
.progress-bar__text-container {
  padding: 0.5rem 1rem;
}
.progress-bar-fill {
  height: 8px;
  border-radius: 4px;
  background: #1899d5;
}
.progress-bar__select-container select {
  padding: 0.3rem 0.7rem;
  border-radius: 4px;
  border: none;
  color: #1899d5;
  font-weight: bold;
}
.white {
  color: #fff;
}
</style>

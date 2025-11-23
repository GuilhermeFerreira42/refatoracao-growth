<template>
  <div class="header-main-container">
    <a href="https://www.gsuplementos.com.br/" aria-label="Ir para a página inicial" class="header-logo">
      <img src="https://via.placeholder.com/800x600/CCCCCC/808080.png?text=IMAGEM_SUBSTITUIDA" alt="Growth" width="158.44" height="49.22" />
    </a>
    <div class="header-search">
      <form>
        <label for="busca-principal-topo" class="visually-hidden">Buscar produto</label>
        <input id="busca-principal-topo" type="text" placeholder="Encontre o suplemento ideal para você" />
        <button type="submit" title="buscar" aria-label="Buscar no site">
          <img src="https://via.placeholder.com/800x600/CCCCCC/808080.png?text=IMAGEM_SUBSTITUIDA" alt="Buscar" width="19.5" height="18.5" />
        </button>
      </form>
    </div>
    <div class="header-icons">
      <div class="header-icon-user">
        <img src="https://via.placeholder.com/800x600/CCCCCC/808080.png?text=IMAGEM_SUBSTITUIDA" alt="Ícone usuário" width="27.68" height="27.68" />
        <p>
          <a href="https://www.gsuplementos.com.br/checkout/cadastro/">Cadastre-se</a> ou<br />
          <a href="https://www.gsuplementos.com.br/checkout/acesso/">faça seu login</a>
        </p>
      </div>
      <a href="https://www.gsuplementos.com.br/minha-conta/lista-desejo" class="header-icon-favoritos">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 6.00019C10.2006 3.90317 7.19377 3.2551 4.93923 5.17534C2.68468 7.09558 2.36727 10.3061 4.13778 12.5772C5.60984 14.4654 10.0648 18.4479 11.5249 19.7369C11.6882 19.8811 11.7699 19.9532 11.8652 19.9815C11.9483 20.0062 12.0393 20.0062 12.1225 19.9815C12.2178 19.9532 12.2994 19.8811 12.4628 19.7369C13.9229 18.4479 18.3778 14.4654 19.8499 12.5772C21.6204 10.3061 21.3417 7.07538 19.0484 5.17534C16.7551 3.2753 13.7994 3.90317 12 6.00019Z" stroke="#fff" stroke-width="1.8"/></svg>
        <span>Favoritos</span>
      </a>
      <div class="header-icon-phone">
        <img src="https://via.placeholder.com/800x600/CCCCCC/808080.png?text=IMAGEM_SUBSTITUIDA" alt="Ícone telefone" width="27.39" height="27.45" />
        <div class="header-fale-conosco">
          <a href="https://www.gsuplementos.com.br/fale-conosco">Fale Conosco<br />Clique aqui</a>
        </div>
      </div>
      <button aria-label="Abrir meu carrinho de compras" class="header-icon-cart">
        <svg width="51.158" height="44.663" viewBox="0 0 51.158 44.663"><circle cx="14.665" cy="14.665" r="13.665" stroke="#1899d5" stroke-width="2" fill="none"/><path d="M16.364,32.182A2.182,2.182,0,1,1,14.182,30,2.182,2.182,0,0,1,16.364,32.182Z" fill="none" stroke="#fff" stroke-width="2"/><path d="M32.864,32.182A2.182,2.182,0,1,1,30.682,30,2.182,2.182,0,0,1,32.864,32.182Z" fill="none" stroke="#fff" stroke-width="2"/><path d="M1.5,1.5H8.01l4.362,15.306c.307,1.086,1.679,1.862,3.255,1.84h15.82c1.577.021,2.948-.754,3.255-1.84l2.6-9.591H9.638" fill="none" stroke="#fff" stroke-width="2"/></svg>
        <span>0</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HeaderMain',
};
</script>

<style scoped>
.header-main-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 35px 0;
  background-color: var(--corPrincipal, #1899d5);
}
.header-logo img {
  height: 49px;
}
.header-search form {
  display: flex;
  background: #fff;
  border-radius: 5px;
  overflow: hidden;
}
.header-search input {
  border: none;
  padding: 10px;
  font-size: 16px;
}
.header-search button {
  background: none;
  border: none;
  width: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.header-icons {
  display: flex;
  align-items: center;
  gap: 24px;
}
.header-icon-user, .header-icon-phone {
  display: flex;
  align-items: center;
  gap: 8px;
}
.header-icon-favoritos {
  display: flex;
  align-items: center;
  color: #fff;
  font-weight: 700;
  gap: 4px;
  text-decoration: none;
}
.header-icon-cart {
  background: none;
  border: none;
  position: relative;
  max-width: 55px;
}
.header-icon-cart span {
  color: #fff;
  font-size: 17px;
  position: absolute;
  left: 23px;
  top: 5.5px;
  width: 27px;
  text-align: center;
}
.visually-hidden {
  clip: rect(0,0,0,0);
  border: 0;
  height: 1px;
  margin: -1px;
  overflow: hidden;
  padding: 0;
  position: absolute;
  white-space: nowrap;
  width: 1px;
}
</style>

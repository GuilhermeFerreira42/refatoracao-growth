<template>
  <div class="menuBarWeContainer">
    <nav class="menu-bar">
      <ul class="menu-list">
        <li class="menu-item destaque">
          <a href="#" class="menu-link">
            <svg class="menu-icon" width="22" height="18" viewBox="0 0 22.5 18.824"><g><line x2="14.5" y1="2" y2="2" stroke="#000" stroke-width="3"/><line x2="19.5" y1="9" y2="9" stroke="#000" stroke-width="3"/><line x2="14.624" y1="16" y2="16" stroke="#000" stroke-width="3"/></g></svg>
            Categorias
            <svg class="arrow-icon" width="12" height="7" viewBox="0 0 12 7"><path d="M1 1l5 5 5-5" stroke="#000" stroke-width="2" fill="none"/></svg>
          </a>
          <ul class="submenu">
            <li><a href="#">Proteínas</a></li>
            <li><a href="#">Aminoácidos</a></li>
            <li><a href="#">Vitaminas</a></li>
            <li><a href="#">Termogênicos</a></li>
          </ul>
        </li>
        <li class="menu-item"><a href="#" class="menu-link">Top 20</a></li>
        <li class="menu-item"><a href="#" class="menu-link">Lançamentos</a></li>
        <li class="menu-item"><a href="#" class="menu-link">Whey Protein</a></li>
        <li class="menu-item"><a href="#" class="menu-link">Creatina</a></li>
        <li class="menu-item"><a href="#" class="menu-link">Pré-treino</a></li>
      </ul>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'MenuBar'
}
</script>

<style scoped>
.menuBarWeContainer {
  width: 100%;
  max-width: var(--weGridWidth, 1670px);
  margin: 0 auto;
  padding: 0 5px;
  display: flex;
  justify-content: center;
}
.menu-bar {
  background: #fff;
  box-shadow: 0 1px 10px rgba(0,0,0,.08);
  margin-top: 10px;
  width: 100%;
  border-radius: 8px;
}
.menu-list {
  display: flex;
  justify-content: flex-start;
  gap: 2rem;
  list-style: none;
  margin: 0;
  padding: 0;
}
.menu-item {
  position: relative;
}
.menu-link {
  color: #1899d5;
  font-weight: bold;
  text-transform: uppercase;
  text-decoration: none;
  font-size: 1rem;
  padding: 10px 0;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: color 0.2s;
}
.menu-link:hover {
  color: #0056b3;
}
.menu-item.destaque .menu-link {
  color: #000;
  font-weight: 700;
}
.menu-icon {
  margin-right: 8px;
}
.arrow-icon {
  margin-left: 8px;
}
.submenu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  background: #fff;
  box-shadow: 0 3px 6px rgba(0,0,0,.16);
  border-radius: 8px;
  min-width: 180px;
  z-index: 10;
  padding: 1rem 0;
}
.menu-item.destaque:hover .submenu,
.menu-item.destaque:focus-within .submenu {
  display: block;
}
.submenu li {
  padding: 0.5rem 1.5rem;
}
.submenu li a {
  color: #1899d5;
  font-weight: 500;
  text-decoration: none;
  font-size: 1rem;
  display: block;
}
.submenu li a:hover {
  color: #0056b3;
}
@media (max-width: 1023px) {
  .menuBarWeContainer {
    padding: 0 10px;
  }
  .menu-list {
    flex-direction: column;
    gap: 0.5rem;
  }
  .menu-bar {
    padding: 0 10px;
    border-radius: 0;
  }
  .submenu {
    position: static;
    box-shadow: none;
    border-radius: 0;
    min-width: 100%;
    padding: 0.5rem 0;
  }
}
</style>

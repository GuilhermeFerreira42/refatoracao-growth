<template>
  <a href="https://www.gsuplementos.com.br/black-growth" class="marquee" style="--6d4f839e:80px">
    <div class="marquee-first-wave">
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
    </div>
    <div class="marquee-second-wave">
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
      <span class="marquee-text">Black + Growth</span>
    </div>
  </a>
</template>

<script>
export default {
  name: 'MarqueeBar',
};
</script>

<style scoped>
.marquee {
  background: #001d45;
  display: block;
  height: 32px;
  overflow: hidden;
  position: relative;
  white-space: nowrap;
  width: 100%;
}
.marquee-first-wave, .marquee-second-wave {
  display: inline-block;
  left: 0;
  position: absolute;
  top: 9px;
  width: max-content;
}
.marquee-first-wave {
  animation: scroll 50s linear infinite reverse;
}
.marquee-second-wave {
  animation: scroll2 50s linear infinite reverse;
}
.marquee-text {
  color: #fff;
  font-size: 16px;
  font-weight: 400;
  line-height: 1;
  margin-right: var(--6d4f839e);
  text-transform: uppercase;
  user-select: none;
  white-space: nowrap;
  width: fit-content;
}
.marquee-first-wave .marquee-text:nth-of-type(odd),
.marquee-second-wave .marquee-text:nth-of-type(2n) {
  font-weight: 700;
}
@keyframes scroll {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(0); }
}
@keyframes scroll2 {
  0% { transform: translateX(0); }
  100% { transform: translateX(100%); }
}
@media (max-width:1023px) {
  .marquee-text { font-size: 14px; }
}
</style>

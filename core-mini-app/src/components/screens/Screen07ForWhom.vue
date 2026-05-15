<script setup>
import { inject } from 'vue'
import HeroLogo from '../HeroLogo.vue'

const goTo = inject('goTo')
</script>

<template>
  <section class="screen">
    <div class="screen-inner">
      <div class="content-card">
        <div class="hero-logo-stack">
          <div class="hero-logo-shell">
            <HeroLogo />
          </div>
          <div class="screen-kicker center">07 — Для кого</div>
        </div>
        <h2 class="section-heading">Кому подходит Ядро</h2>
        <div class="section-divider"><span></span></div>
        <div class="list-block">
          <div class="list-item"><span class="bullet">▪️</span><span>Тем, кто устал всё понимать, но мало менять</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Тем, кто чувствует, что их потенциал выше текущей жизни</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Тем, кто хочет не мотивацию на 2 дня, а устойчивую внутреннюю перестройку</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Тем, кто готов к честному движению и сильной среде</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Тем, кто хочет расти не только в деньгах, но и в качестве личности</span></div>
        </div>

        <h3 style="margin-top: 26px; text-align: center;">Кому не подойдёт</h3>
        <div class="list-block">
          <div class="list-item"><span class="bullet">▪️</span><span>Тем, кто ищет волшебную таблетку</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Тем, кто хочет просто "послушать что-нибудь полезное"</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Тем, кто не готов к практике, включённости и честной обратной связи</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Тем, кто хочет всё и сразу, но не готов строить основу</span></div>
        </div>

        <div class="button-row">
          <button class="btn btn-ghost" @click="goTo(6)">НАЗАД</button>
          <button class="btn btn-primary" @click="goTo(8)">ФОРМАТЫ УЧАСТИЯ</button>
        </div>
      </div>
    </div>
  </section>
</template>

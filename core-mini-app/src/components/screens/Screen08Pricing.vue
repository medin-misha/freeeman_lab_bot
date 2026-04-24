<script setup>
import { inject } from 'vue'
import HeroLogo from '../HeroLogo.vue'

const goTo = inject('goTo')
</script>

<template>
  <section class="screen">
    <div class="screen-inner">
      <HeroLogo />
      <div class="content-card">
        <h2>Форматы участия</h2>
        <p>Сейчас ты можешь зайти в Ядро по стартовой стоимости. Это ранний этап проекта, и именно поэтому вход сейчас доступнее.</p>
        <p>Дальше пространство будет расти: будет больше глубины, больше модулей, больше инструментов, больше экспертов и больше ценности внутри. По мере развития проекта цена участия также будет повышаться.</p>

        <div class="price-box">
          <div class="price-grid">
            <div class="price-card">
              <div class="price-label">1 месяц</div>
              <div class="price-value">2 500 ₽</div>
              <div class="price-note">Чтобы зайти, почувствовать ритм пространства и начать движение.</div>
            </div>
            <div class="price-card featured">
              <div class="price-badge">Рекомендуемый формат</div>
              <div class="price-label">3 месяца</div>
              <div class="price-value">6 000 ₽</div>
              <div class="price-note">Чтобы не просто попробовать, а войти в более устойчивую динамику, закрепить базу и пройти глубже.</div>
            </div>
          </div>
        </div>

        <div class="micro-accent">Вход в Ядро не массовый. Он идёт через анкету и личное рассмотрение заявки.</div>

        <div class="button-row">
          <button class="btn btn-primary" @click="goTo(9)">ПЕРЕЙТИ К АНКЕТЕ</button>
        </div>
      </div>
    </div>
  </section>
</template>

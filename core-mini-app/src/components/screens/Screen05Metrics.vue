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
        <h2>Мы не гадаем, растёшь ты или просто красиво думаешь об этом</h2>
        <p>Главная особенность Ядра — здесь рост не остаётся ощущением или самоуспокоением.</p>
        <p>На входе человек проходит диагностику. Дальше мы смотрим на динамику по ключевым сферам. Это позволяет увидеть, где действительно идёт движение, а где человек по-прежнему ходит по кругу, просто более умными словами объясняя себе то же самое.</p>
        <p>Здесь сложнее имитировать рост. Потому что система постепенно показывает твою реальную внутреннюю картину.</p>
        <div class="metric-grid">
          <div class="metric-card">Состояние и энергия</div>
          <div class="metric-card">Дисциплина и ритм</div>
          <div class="metric-card">Речь и внутренняя позиция</div>
          <div class="metric-card">Проявленность и видимость</div>
          <div class="metric-card">Отношения и границы</div>
          <div class="metric-card">Деньги и реализация</div>
        </div>
        <div class="micro-accent">По мере роста проекта система замеров, сопровождения и глубины будет усиливаться.</div>
        <div class="button-row">
          <button class="btn btn-ghost" @click="goTo(4)">НАЗАД</button>
          <button class="btn btn-primary" @click="goTo(6)">ФОРМАТ РАБОТЫ</button>
        </div>
      </div>
    </div>
  </section>
</template>

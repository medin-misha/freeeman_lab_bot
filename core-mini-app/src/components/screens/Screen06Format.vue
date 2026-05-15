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
          <div class="screen-kicker center">06 — Формат работы</div>
        </div>
        <h2 class="section-heading">Как устроена работа внутри</h2>
        <div class="section-divider"><span></span></div>
        <div class="section-copy">
          <p>Формат Ядра строится не вокруг пассивного потребления, а вокруг включённости.</p>
          <p>Внутри тебя ждёт не просто контент, а рабочая среда, где есть ритм, отражение, практика, сопровождение и движение по ключевым зонам роста.</p>
        </div>
        <div class="list-block">
          <div class="list-item"><span class="bullet">▪️</span><span>Еженедельные живые эфиры</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Практики и задания на внедрение</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Работа по разным направлениям личности</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Мини-группы и живой контакт</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Напарник или buddy для движения в ритме</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Разборы, наблюдение и обратная связь</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Постепенное усиление глубины внутри проекта</span></div>
        </div>
        <div class="micro-accent">Это пространство подойдёт тем, кто готов входить в процесс, а не просто наблюдать со стороны.</div>
        <div class="button-row">
          <button class="btn btn-ghost" @click="goTo(5)">НАЗАД</button>
          <button class="btn btn-primary" @click="goTo(7)">КОМУ ПОДХОДИТ ЯДРО</button>
        </div>
      </div>
    </div>
  </section>
</template>

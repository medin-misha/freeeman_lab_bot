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
          <div class="screen-kicker center">04 — Логика пути</div>
        </div>
        <h2 class="section-heading">Путь внутри Ядра строится поэтапно</h2>
        <div class="section-divider"><span></span></div>
        <div class="section-copy">
          <p>Мы не пытаемся сразу лезть в самую глубокую точку, если у человека не собрана база. Потому что масштаб не держится на вдохновении. Он держится на конструкции.</p>
          <p>Поэтому движение внутри Ядра идёт по живой логике:</p>
          <p>Сначала ты собираешь основу: режим, тело, внимание, устойчивость, базовую дисциплину, способность выдерживать нагрузку и не рассыпаться. Потом становится видно, где у тебя узкое горлышко: в эмоциях, в речи, в мышлении, в страхе, в действиях, в идентичности, в тени, в отношениях, в деньгах или в проявленности.</p>
          <p>Дальше начинается уже более точная работа: проработка, практика, интеграция, перестройка привычных паттернов. И только на этой базе человек начинает по-настоящему проявляться, усиливать влияние, двигаться в реализации, в деньгах и в более крупном масштабе жизни.</p>
        </div>
        <div class="list-block">
          <div class="list-item"><span class="bullet">▪️</span><span>Сначала — база</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Потом — честная диагностика узких мест</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Затем — проработка и интеграция</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Далее — проявленность, влияние, деньги, реализация</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>И в итоге — движение в больший масштаб личности</span></div>
        </div>
        <div class="button-row">
          <button class="btn btn-ghost" @click="goTo(3)">НАЗАД</button>
          <button class="btn btn-primary" @click="goTo(5)">КАК МЫ ПОНИМАЕМ, ЧТО ЕСТЬ РОСТ</button>
        </div>
      </div>
    </div>
  </section>
</template>

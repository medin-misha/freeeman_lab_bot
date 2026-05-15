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
          <div class="screen-kicker center">03 — Что внутри</div>
        </div>
        <h2 class="section-heading">Что происходит внутри Ядра</h2>
        <div class="section-divider"><span></span></div>
        <div class="section-copy">
          <p>Ядро — это не просто чат, не архив материалов и не одноразовый интенсив. Это живая среда, которая будет постепенно расти, усиливаться и раскрываться месяц за месяцем.</p>
          <p>Ты заходишь не в "готовую коробку", а в пространство, в которое я вкладываю время, внимание, глубину и систему. Сейчас вход доступен по более низкой цене именно потому, что проект находится в активной стадии роста. Дальше внутри будет больше глубины, больше инструментов, больше экспертов, больше направлений и, соответственно, выше стоимость участия.</p>
          <p>Здесь работа строится не по одной теме, а по целому контуру личности.</p>
        </div>
        <div class="list-block">
          <div class="list-item"><span class="bullet">▪️</span><span>База: тело, режим, питание, восстановление, устойчивость</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Состояние: энергия, стресс, внутренний ритм</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Эмоции: контейнирование, регуляция, проживание</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Язык и мышление: речь, формулировки, внутренний диалог</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Действие: страх, откладывание, запуск, удержание курса</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Идентичность: старые роли, внутренние режимы, взросление</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Тень: подавленная энергия, стыд, агрессия, самосокрытие</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Род и семья: сценарии, иерархия, привязанность, передача</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Проявленность: страх быть видимым, голос, позиция, влияние</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Деньги и реализация: потолок дохода, ценность, движение в социуме</span></div>
        </div>
        <div class="button-row">
          <button class="btn btn-ghost" @click="goTo(2)">НАЗАД</button>
          <button class="btn btn-primary" @click="goTo(4)">КАК СТРОИТСЯ ПУТЬ ВНУТРИ</button>
        </div>
      </div>
    </div>
  </section>
</template>

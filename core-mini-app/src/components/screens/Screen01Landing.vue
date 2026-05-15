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
          <div class="screen-kicker center">Закрытое пространство</div>
        </div>
        <h1 class="hero-heading">Ядро — закрытое пространство для тех, кто больше не хочет имитировать рост</h1>
        <div class="section-divider"><span></span></div>
        <div class="video-shell">
          <div class="video-wrap">
            <iframe
              src="https://rutube.ru/play/embed/f3f760fd882135480fabb2a0f5469a47/"
              allow="clipboard-write; autoplay; fullscreen"
              allowfullscreen
              title="Видео"
            ></iframe>
          </div>
        </div>
        <div class="hero-copy-stack">
          <p class="lead-text">Не ещё одна теория.</p>
          <p class="lead-text">Не ещё один красивый мотивационный заход.</p>
          <p class="lead-text">Это пространство, где ты начинаешь собирать себя в ритм, в опору, в действие и в реальную внутреннюю динамику.</p>
        </div>
        <div class="button-row">
          <button class="btn btn-primary" @click="goTo(2)">УЗНАТЬ ПОДРОБНЕЕ</button>
        </div>
      </div>
    </div>
  </section>
</template>

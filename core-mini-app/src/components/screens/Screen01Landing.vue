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
        <h1>Ядро — закрытое пространство для тех, кто больше не хочет имитировать рост</h1>
        <div class="video-shell">
          <div class="video-wrap">
            <iframe
              src="https://rutube.ru/play/embed/6d6df53a0c4406832c7b4f38d3198c57/"
              allow="clipboard-write; autoplay; fullscreen"
              allowfullscreen
              title="Видео"
            ></iframe>
          </div>
        </div>
        <p class="lead-text">
          Не ещё одна теория.<br>
          Не ещё один красивый мотивационный заход.<br>
          Это пространство, где ты начинаешь собирать себя в ритм, в опору, в действие и в реальную внутреннюю динамику.
        </p>
        <div class="button-row">
          <button class="btn btn-primary" @click="goTo(2)">УЗНАТЬ ПОДРОБНЕЕ</button>
        </div>
      </div>
    </div>
  </section>
</template>

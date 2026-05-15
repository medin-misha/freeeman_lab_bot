<script setup>
import { useTelegram } from '../composables/useTelegram.js'
import HeroLogo from './HeroLogo.vue'

const { close } = useTelegram()
const waitingListUrl = 'https://t.me/+uJbJ9thccCM0ZDBi'

function openWaitingList() {
  window.location.href = waitingListUrl
}
</script>

<template>
  <section class="screen">
    <div class="screen-inner">
      <div class="success-panel">
        <div class="success-logo-wrap">
          <HeroLogo class="success-logo" />
        </div>
        <div class="screen-kicker center success-heading">Заявка отправлена</div>
        <h2 class="section-heading">Спасибо. Я лично посмотрю твою анкету.</h2>
        <div class="section-divider"><span></span></div>
        <div class="success-box section-copy">
          <p>Спасибо. Я лично посмотрю твою анкету и приму решение по входу.</p>
          <p>Если почувствую, что формат тебе подходит, ты получишь дальнейшую информацию по участию. Ядро — это не массовый вход, а пространство, которое собирается осознанно.</p>
        </div>
        <div class="success-note">Приложение можно закрыть</div>
        <div class="button-row stack">
          <button class="btn btn-ghost" @click="openWaitingList">ЯДРО | ЛИСТ ОЖИДАНИЯ</button>
          <button class="btn btn-primary" @click="close">ЗАКРЫТЬ</button>
        </div>
      </div>
    </div>
  </section>
</template>

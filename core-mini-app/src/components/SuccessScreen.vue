<script setup>
import { useTelegram } from '../composables/useTelegram.js'

const { close } = useTelegram()
</script>

<template>
  <section class="screen">
    <div class="screen-inner">
      <div class="success-logo-wrap">
        <div style="text-align:center; padding-top: 50px;">
          <img
            src="https://i.postimg.cc/4yfy9nb4/Adro-(LOGO)-Photoroom.png"
            style="width: 250px; margin-bottom: 30px;"
            alt="Логотип"
            class="success-logo"
          />
        </div>
      </div>
      <div class="success-box">
        <h2>Заявка принята</h2>
        <p>Спасибо. Я лично посмотрю твою анкету и приму решение по входу.</p>
        <p>Если почувствую, что формат тебе подходит, ты получишь дальнейшую информацию по участию. Ядро — это не массовый вход, а пространство, которое собирается осознанно.</p>
        <div class="success-note">Приложение можно закрыть</div>
        <div class="button-row">
          <button class="btn btn-ghost" @click="close">ВЕРНУТЬСЯ В БОТ</button>
          <button class="btn btn-primary" @click="close">ЗАКРЫТЬ</button>
        </div>
      </div>
    </div>
  </section>
</template>

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
        <h2>Ты можешь много понимать — и всё равно стоять на месте</h2>
        <div class="section-text">
          <p>Большинство людей сегодня не страдают от нехватки информации. Они страдают от расфокуса, внутреннего распада, перегруза, отсутствия среды и невозможности перевести понимание в реальную жизнь.</p>
          <p>Ядро создано для тех, кто устал бесконечно думать, анализировать, начинать заново и снова откатываться. Это закрытое пространство для людей, которые хотят не казаться растущими, а действительно меняться — в состоянии, в дисциплине, в проявленности, в деньгах, в качестве решений и в масштабе своей личности.</p>
        </div>
        <div class="list-block">
          <div class="list-item"><span class="bullet">▪️</span><span>Выйти из внутреннего расфокуса</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Перестать жить рывками и откатами</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Собрать опору, ритм и взрослую позицию</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Двигаться не в одиночку, а в сильной среде</span></div>
          <div class="list-item"><span class="bullet">▪️</span><span>Переводить понимание в реальные изменения</span></div>
        </div>
        <div class="button-row">
          <button class="btn btn-ghost" @click="goTo(1)">НАЗАД</button>
          <button class="btn btn-primary" @click="goTo(3)">ЧТО ПРОИСХОДИТ ВНУТРИ</button>
        </div>
      </div>
    </div>
  </section>
</template>

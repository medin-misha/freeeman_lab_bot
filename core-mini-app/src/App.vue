<script setup>
import { ref, provide, onMounted } from 'vue'
import { useTelegram } from './composables/useTelegram.js'

import SplashScreen from './components/SplashScreen.vue'
import SuccessScreen from './components/SuccessScreen.vue'

import Screen01Landing from './components/screens/Screen01Landing.vue'
import Screen02Problem from './components/screens/Screen02Problem.vue'
import Screen03Inside from './components/screens/Screen03Inside.vue'
import Screen04Path from './components/screens/Screen04Path.vue'
import Screen05Metrics from './components/screens/Screen05Metrics.vue'
import Screen06Format from './components/screens/Screen06Format.vue'
import Screen07ForWhom from './components/screens/Screen07ForWhom.vue'
import Screen08Pricing from './components/screens/Screen08Pricing.vue'

import FormStep01 from './components/form/FormStep01.vue'
import FormStep02 from './components/form/FormStep02.vue'
import FormStep03 from './components/form/FormStep03.vue'
import FormStep04 from './components/form/FormStep04.vue'
import FormStep05 from './components/form/FormStep05.vue'
import FormStep06 from './components/form/FormStep06.vue'

const { initApp, haptic } = useTelegram()
const currentScreen = ref(0)

function goTo(n) {
  haptic()
  currentScreen.value = n
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

provide('goTo', goTo)

onMounted(() => {
  initApp()
  setTimeout(() => goTo(1), 1800)
})
</script>

<template>
  <div class="app">
    <SplashScreen    v-if="currentScreen === 0" />
    <Screen01Landing v-else-if="currentScreen === 1" />
    <Screen02Problem v-else-if="currentScreen === 2" />
    <Screen03Inside  v-else-if="currentScreen === 3" />
    <Screen04Path    v-else-if="currentScreen === 4" />
    <Screen05Metrics v-else-if="currentScreen === 5" />
    <Screen06Format  v-else-if="currentScreen === 6" />
    <Screen07ForWhom v-else-if="currentScreen === 7" />
    <Screen08Pricing v-else-if="currentScreen === 8" />
    <FormStep01      v-else-if="currentScreen === 9" />
    <FormStep02      v-else-if="currentScreen === 10" />
    <FormStep03      v-else-if="currentScreen === 11" />
    <FormStep04      v-else-if="currentScreen === 12" />
    <FormStep05      v-else-if="currentScreen === 13" />
    <FormStep06      v-else-if="currentScreen === 14" />
    <SuccessScreen   v-else-if="currentScreen === 15" />
  </div>
</template>

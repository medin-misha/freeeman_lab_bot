<script setup>
import { ref, inject } from 'vue'
import { formData, useForm } from '../../composables/useForm.js'
import FormHeader from '../FormHeader.vue'
import SelectionCard from '../SelectionCard.vue'

const goTo = inject('goTo')
const { validateStep } = useForm()
const error = ref('')

const options = [
  'Дисциплина', 'Энергия', 'Состояние', 'Проявленность',
  'Речь', 'Мышление', 'Отношения', 'Внутренняя опора',
  'Деньги', 'Реализация'
]

function next() {
  const msg = validateStep(3)
  if (msg) { error.value = msg; return }
  error.value = ''
  goTo(12)
}
</script>

<template>
  <section class="screen">
    <div class="screen-inner">
      <div class="content-card">
        <FormHeader :step="3" />
        <div class="form-intro">
          <div class="form-kicker">Шаг 03</div>
          <h3>Приоритеты роста</h3>
          <p class="form-subtitle">Что для тебя сейчас важнее всего усилить?</p>
        </div>
        <div class="selection-grid two-col">
          <SelectionCard
            v-for="opt in options"
            :key="opt"
            type="checkbox"
            name="priorities"
            :value="opt"
            :label="opt"
            v-model="formData.priorities"
          />
        </div>
        <div class="error-text">{{ error }}</div>
        <div class="button-row">
          <button class="btn btn-ghost" @click="goTo(10)">НАЗАД</button>
          <button class="btn btn-primary" @click="next">ДАЛЕЕ</button>
        </div>
      </div>
    </div>
  </section>
</template>

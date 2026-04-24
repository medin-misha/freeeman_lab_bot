<script setup>
import { ref, inject } from 'vue'
import { formData, useForm } from '../../composables/useForm.js'
import FormHeader from '../FormHeader.vue'

const goTo = inject('goTo')
const { validateStep } = useForm()
const error = ref('')

function next() {
  const msg = validateStep(2)
  if (msg) { error.value = msg; return }
  error.value = ''
  goTo(11)
}
</script>

<template>
  <section class="screen">
    <div class="screen-inner">
      <div class="content-card">
        <FormHeader :step="2" />
        <h3>Точка входа</h3>
        <div class="field-group">
          <label class="field-label" for="request">Что в твоей жизни сейчас требует самого сильного сдвига?</label>
          <textarea
            class="textarea"
            id="request"
            v-model="formData.request"
            placeholder="Опиши, где ты сейчас больше всего буксуешь или что хочешь изменить в первую очередь"
          ></textarea>
        </div>
        <div class="error-text">{{ error }}</div>
        <div class="button-row">
          <button class="btn btn-ghost" @click="goTo(9)">НАЗАД</button>
          <button class="btn btn-primary" @click="next">ДАЛЕЕ</button>
        </div>
      </div>
    </div>
  </section>
</template>

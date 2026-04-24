<script setup>
import { ref, inject } from 'vue'
import { formData, useForm } from '../../composables/useForm.js'
import FormHeader from '../FormHeader.vue'

const goTo = inject('goTo')
const { validateStep } = useForm()
const error = ref('')

function next() {
  const msg = validateStep(4)
  if (msg) { error.value = msg; return }
  error.value = ''
  goTo(13)
}
</script>

<template>
  <section class="screen">
    <div class="screen-inner">
      <div class="content-card">
        <FormHeader :step="4" />
        <h3>Мотивация</h3>
        <div class="field-group">
          <label class="field-label" for="motivation">Почему тебе важно попасть в Ядро именно сейчас, а не когда-нибудь потом?</label>
          <textarea
            class="textarea"
            id="motivation"
            v-model="formData.motivation"
            placeholder="Опиши, почему этот этап для тебя сейчас важен и почему ты хочешь зайти именно в это пространство"
          ></textarea>
        </div>
        <div class="error-text">{{ error }}</div>
        <div class="button-row">
          <button class="btn btn-ghost" @click="goTo(11)">НАЗАД</button>
          <button class="btn btn-primary" @click="next">ДАЛЕЕ</button>
        </div>
      </div>
    </div>
  </section>
</template>

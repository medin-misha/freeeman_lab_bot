<script setup>
import { ref, inject } from 'vue'
import { formData, useForm } from '../../composables/useForm.js'
import FormHeader from '../FormHeader.vue'

const goTo = inject('goTo')
const { validateStep } = useForm()
const error = ref('')

function next() {
  const msg = validateStep(1)
  if (msg) { error.value = msg; return }
  error.value = ''
  goTo(10)
}
</script>

<template>
  <section class="screen">
    <div class="screen-inner">
      <div class="content-card">
        <FormHeader :step="1" />
        <div class="form-intro">
          <div class="form-kicker">Шаг 01</div>
          <h3>База</h3>
          <p class="form-subtitle">Несколько фактов, чтобы я понимал, кто заходит.</p>
        </div>
        <div class="field-group">
          <label class="field-label" for="full_name">Имя</label>
          <input class="input" type="text" id="full_name" v-model="formData.full_name" placeholder="Введите имя" />
        </div>
        <div class="field-group">
          <label class="field-label" for="birth_date">Дата рождения</label>
          <input class="input" type="date" id="birth_date" v-model="formData.birth_date" />
        </div>
        <div class="field-group">
          <label class="field-label" for="city">Город</label>
          <input class="input" type="text" id="city" v-model="formData.city" placeholder="Ваш город" />
        </div>
        <div class="field-group">
          <label class="field-label" for="activity">Деятельность</label>
          <input class="input" type="text" id="activity" v-model="formData.activity" placeholder="Чем вы занимаетесь" />
        </div>
        <div class="error-text">{{ error }}</div>
        <div class="button-row">
          <button class="btn btn-primary" @click="next">ДАЛЕЕ</button>
        </div>
      </div>
    </div>
  </section>
</template>

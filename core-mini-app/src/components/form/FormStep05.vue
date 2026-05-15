<script setup>
import { ref, inject } from 'vue'
import { formData, useForm } from '../../composables/useForm.js'
import FormHeader from '../FormHeader.vue'

const goTo = inject('goTo')
const { validateStep } = useForm()
const error = ref('')

function next() {
  const msg = validateStep(5)
  if (msg) { error.value = msg; return }
  error.value = ''
  goTo(14)
}
</script>

<template>
  <section class="screen">
    <div class="screen-inner">
      <div class="content-card">
        <FormHeader :step="5" />
        <div class="form-intro">
          <div class="form-kicker">Шаг 05</div>
          <h3>Честность с собой</h3>
          <p class="form-subtitle">Что обычно мешает тебе удерживать ритм и не сойти с дистанции?</p>
        </div>
        <div class="field-group">
          <label class="field-label" for="difficulties">Что обычно мешает тебе удерживать ритм и не сойти с дистанции?</label>
          <textarea
            class="textarea"
            id="difficulties"
            v-model="formData.difficulties"
            placeholder="Опиши свои типичные откаты, срывы, слабые места или то, где ты чаще всего теряешь движение"
          ></textarea>
        </div>
        <div class="error-text">{{ error }}</div>
        <div class="button-row">
          <button class="btn btn-ghost" @click="goTo(12)">НАЗАД</button>
          <button class="btn btn-primary" @click="next">ДАЛЕЕ</button>
        </div>
      </div>
    </div>
  </section>
</template>

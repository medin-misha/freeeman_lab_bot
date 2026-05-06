<script setup>
import { ref, inject } from 'vue'
import { formData, useForm } from '../../composables/useForm.js'
import { useTelegram } from '../../composables/useTelegram.js'
import FormHeader from '../FormHeader.vue'
import SelectionCard from '../SelectionCard.vue'

const goTo = inject('goTo')
const { validateStep, submit } = useForm()
const { haptic } = useTelegram()

const error = ref('')
const submitError = ref('')
const submitting = ref(false)

async function handleSubmit() {
  const msg = validateStep(6)
  if (msg) { error.value = msg; return }
  error.value = ''
  submitError.value = ''

  haptic()
  submitting.value = true
  try {
    await submit()
    goTo(15)
  } catch (e) {
    console.error('Ошибка отправки:', e)
    submitError.value = 'Не удалось отправить заявку. Проверь соединение и попробуй ещё раз. Экран подтверждения появится только после успешной отправки. Если ошибка не исчезает, обратись к @it_was_i_misha.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <section class="screen">
    <div class="screen-inner">
      <div class="content-card">
        <FormHeader :step="6" />
        <h3>Готовность к формату</h3>

        <div class="question-block">
          <div class="question-title">Готовность быть в процессе</div>
          <div class="selection-grid">
            <SelectionCard
              name="readiness"
              value="Готов(а) быть включённо и регулярно"
              label="Готов(а) быть включённо и регулярно"
              v-model="formData.readiness"
            />
            <SelectionCard
              name="readiness"
              value="Смогу быть в процессе частично, но стабильно"
              label="Смогу быть в процессе частично, но стабильно"
              v-model="formData.readiness"
            />
          </div>
        </div>

        <div class="question-block">
          <div class="question-title">Сколько времени в неделю ты реально готов(а) выделять?</div>
          <div class="selection-grid">
            <SelectionCard
              name="weekly_time"
              value="До 3 часов в неделю"
              label="До 3 часов в неделю"
              v-model="formData.weekly_time"
            />
            <SelectionCard
              name="weekly_time"
              value="От 3 до 5 часов в неделю"
              label="От 3 до 5 часов в неделю"
              v-model="formData.weekly_time"
            />
            <SelectionCard
              name="weekly_time"
              value="Более 5 часов в неделю"
              label="Более 5 часов в неделю"
              v-model="formData.weekly_time"
            />
          </div>
        </div>

        <div class="question-block">
          <div class="question-title">Отношение к формату</div>
          <div class="selection-grid">
            <SelectionCard
              name="rules"
              value="Готов(а) входить в процесс честно, без имитации участия"
              label="Готов(а) входить в процесс честно, без имитации участия"
              v-model="formData.rules"
            />
            <SelectionCard
              name="rules"
              value="Хочу сначала лучше понять формат и правила участия"
              label="Хочу сначала лучше понять формат и правила участия"
              v-model="formData.rules"
            />
          </div>
        </div>

        <div class="question-block">
          <div class="question-title">Формат оплаты</div>
          <div class="selection-grid">
            <SelectionCard
              name="payment"
              value="Готов(а) оплатить 1 месяц"
              label="Готов(а) оплатить 1 месяц"
              v-model="formData.payment"
            />
            <SelectionCard
              name="payment"
              value="Готов(а) оплатить 3 месяца"
              label="Готов(а) оплатить 3 месяца"
              v-model="formData.payment"
            />
            <SelectionCard
              name="payment"
              value="Хочу обсудить формат участия"
              label="Хочу обсудить формат участия"
              v-model="formData.payment"
            />
          </div>
        </div>

        <div class="error-text">{{ error }}</div>
        <div v-if="submitError" class="submit-error active">{{ submitError }}</div>

        <div class="button-row">
          <button class="btn btn-ghost" @click="goTo(13)">НАЗАД</button>
          <button class="btn btn-primary" :disabled="submitting" @click="handleSubmit">
            {{ submitting ? 'ОТПРАВКА...' : 'ОТПРАВИТЬ ЗАЯВКУ' }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

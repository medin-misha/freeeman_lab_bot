import { reactive } from 'vue'
import { useTelegram } from './useTelegram.js'

const API_URL = import.meta.env.VITE_API_URL

export const formData = reactive({
  full_name: '',
  birth_date: '',
  city: '',
  activity: '',
  request: '',
  priorities: [],
  motivation: '',
  difficulties: '',
  readiness: '',
  weekly_time: '',
  rules: '',
  payment: '',
  telegram_id: '',
})

export function useForm() {
  const { getUser } = useTelegram()

  function validateStep(step) {
    if (step === 1) {
      if (!formData.full_name || !formData.birth_date || !formData.city || !formData.activity) {
        return 'Пожалуйста, заполните все поля, чтобы перейти дальше.'
      }
    }
    if (step === 2) {
      if (!formData.request) return 'Опиши свою текущую точку, чтобы продолжить.'
    }
    if (step === 3) {
      if (!formData.priorities.length) return 'Выбери хотя бы один приоритет.'
    }
    if (step === 4) {
      if (!formData.motivation) return 'Расскажи о своей мотивации.'
    }
    if (step === 5) {
      if (!formData.difficulties) return 'Опиши, что обычно мешает тебе удерживать движение.'
    }
    if (step === 6) {
      if (!formData.readiness || !formData.weekly_time || !formData.rules || !formData.payment) {
        return 'Ответь на все пункты, чтобы отправить заявку.'
      }
    }
    return null
  }

  async function submit() {
    const user = getUser()
    if (user) {
      formData.telegram_id = String(user.id || '')
    }

    const payload = {
      telegram_id: formData.telegram_id,
      full_name: formData.full_name,
      birth_date: formData.birth_date,
      city: formData.city,
      activity: formData.activity,
      request: formData.request,
      priorities: formData.priorities,
      motivation: formData.motivation,
      difficulties: formData.difficulties,
      readiness: formData.readiness,
      weekly_time: formData.weekly_time,
      rules: formData.rules,
      payment: formData.payment,
    }

    const response = await fetch(`${API_URL}/core/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!response.ok) throw new Error('Webhook response was not ok')
    return response
  }

  return { formData, validateStep, submit }
}

<script setup>
import { computed } from 'vue'
import { useTelegram } from '../composables/useTelegram.js'

const props = defineProps({
  type: { type: String, default: 'radio' },
  name: { type: String, required: true },
  value: { type: String, required: true },
  label: { type: String, required: true },
  modelValue: { type: [String, Array], default: null }
})

const emit = defineEmits(['update:modelValue'])
const { haptic } = useTelegram()

const isChecked = computed(() => {
  if (props.type === 'checkbox') {
    return Array.isArray(props.modelValue) && props.modelValue.includes(props.value)
  }
  return props.modelValue === props.value
})

function onChange(event) {
  haptic()
  if (props.type === 'checkbox') {
    const arr = Array.isArray(props.modelValue) ? [...props.modelValue] : []
    if (event.target.checked) {
      emit('update:modelValue', [...arr, props.value])
    } else {
      emit('update:modelValue', arr.filter(v => v !== props.value))
    }
  } else {
    emit('update:modelValue', props.value)
  }
}
</script>

<template>
  <label :class="['selection-card', type === 'checkbox' ? 'checkbox' : '']">
    <input
      :type="type"
      :name="name"
      :value="value"
      :checked="isChecked"
      @change="onChange"
    />
    <div class="selection-ui">
      <span class="selection-title">{{ label }}</span>
    </div>
  </label>
</template>

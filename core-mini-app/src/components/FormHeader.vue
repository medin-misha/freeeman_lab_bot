<script setup>
import HeroLogo from './HeroLogo.vue'

defineProps({
  step: { type: Number, required: true },
  total: { type: Number, default: 6 }
})
</script>

<template>
  <div class="form-header">
    <span class="form-logo-wrap">
      <HeroLogo class="form-logo" />
    </span>
    <span class="step-badge">ШАГ {{ step }} ИЗ {{ total }}</span>
  </div>
</template>

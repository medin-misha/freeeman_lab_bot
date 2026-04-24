<script setup>
defineProps({
  step: { type: Number, required: true },
  total: { type: Number, default: 6 }
})
</script>

<template>
  <div class="form-header">
    <span class="form-logo-wrap">
      <img
        src="https://i.postimg.cc/4yfy9nbJ/A-(LOGO)-Photoroom.png"
        style="height:40px;"
        alt="Логотип"
        class="form-logo"
      />
    </span>
    <span class="step-badge">ШАГ {{ step }} ИЗ {{ total }}</span>
  </div>
</template>

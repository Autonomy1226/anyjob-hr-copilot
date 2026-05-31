<template>
  <div class="stat-card" :style="{ '--card-color': color }">
    <span class="stat-icon">{{ icon }}</span>
    <div class="stat-body">
      <span class="stat-value">{{ displayValue }}</span>
      <span class="stat-title">{{ title }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  title: string
  value: string | number
  icon: string
  color: string
}>()

const displayValue = computed(() => {
  const v = props.value
  if (typeof v === 'number' && v === 0) return '0'
  return v || '—'
})
</script>

<style scoped>
.stat-card {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--aj-surface);
  border: 1px solid var(--aj-border);
  border-radius: 8px;
  padding: 12px;
  border-left: 3px solid var(--card-color);
}
.stat-icon {
  font-size: 22px;
}
.stat-body {
  display: flex;
  flex-direction: column;
}
.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--aj-text);
}
.stat-title {
  font-size: 11px;
  color: var(--aj-text-secondary);
}
</style>

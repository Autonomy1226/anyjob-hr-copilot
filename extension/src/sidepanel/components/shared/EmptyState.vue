<template>
  <div class="empty-state">
    <span class="empty-icon">&#x1F4CB;</span>
    <p class="empty-text">{{ text }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{ text: string }>()
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 16px;
  text-align: center;
}
.empty-icon {
  font-size: 40px;
  opacity: 0.4;
}
.empty-text {
  margin-top: 8px;
  font-size: 13px;
  color: var(--aj-text-secondary);
}
</style>

<template>
  <div class="loading-spinner">
    <el-icon class="is-loading" :size="32"><Loading /></el-icon>
    <p v-if="text" class="loading-text">{{ text }}</p>
  </div>
</template>

<script setup lang="ts">
import { Loading } from '@element-plus/icons-vue'
defineProps<{ text?: string }>()
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
  color: var(--aj-primary);
}
.loading-text {
  margin-top: 8px;
  font-size: 13px;
  color: var(--aj-text-secondary);
}
</style>

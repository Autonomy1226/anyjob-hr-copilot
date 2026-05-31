<template>
  <header class="sidebar-header">
    <div class="header-brand">
      <span class="header-icon">&#x1F916;</span>
      <span class="header-title">AnyJob HR Copilot</span>
    </div>
    <el-tag :type="backendOnline ? 'success' : 'danger'" size="small" effect="dark">
      {{ backendOnline ? 'Online' : 'Offline' }}
    </el-tag>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'

const backendOnline = ref(false)

onMounted(async () => {
  try {
    const api = useApi()
    await api.healthCheck()
    backendOnline.value = true
  } catch {
    backendOnline.value = false
  }
})
</script>

<style scoped>
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: linear-gradient(135deg, var(--aj-primary), var(--aj-primary-dark));
  color: #fff;
}
.header-brand {
  display: flex;
  align-items: center;
  gap: 8px;
}
.header-icon {
  font-size: 20px;
}
.header-title {
  font-size: 15px;
  font-weight: 600;
}
</style>

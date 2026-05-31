<template>
  <nav class="sidebar-tabs">
    <router-link
      v-for="tab in tabs"
      :key="tab.path"
      :to="tab.path"
      class="tab-item"
      active-class="tab-active"
    >
      <span class="tab-icon">{{ tab.icon }}</span>
      <span class="tab-label">{{ tab.label }}</span>
    </router-link>
  </nav>
</template>

<script setup lang="ts">
const tabs = [
  { path: '/resume', label: '简历解析', icon: '📄' },
  { path: '/matching', label: '人岗匹配', icon: '🎯' },
  { path: '/message', label: '智能消息', icon: '💬' },
  { path: '/dashboard', label: '数据看板', icon: '📊' },
]
</script>

<style scoped>
.sidebar-tabs {
  display: flex;
  background: var(--aj-surface);
  border-bottom: 1px solid var(--aj-border);
  overflow-x: auto;
}
.tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 10px 4px;
  font-size: 11px;
  color: var(--aj-text-secondary);
  text-decoration: none;
  transition: color 0.2s;
  border-bottom: 2px solid transparent;
  white-space: nowrap;
}
.tab-item:hover {
  color: var(--aj-primary);
}
.tab-active {
  color: var(--aj-primary);
  border-bottom-color: var(--aj-primary);
}
.tab-icon {
  font-size: 16px;
}
</style>

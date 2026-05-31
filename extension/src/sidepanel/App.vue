<template>
  <div class="app">
    <SidebarHeader />
    <SidebarTabs />
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import SidebarHeader from './components/layout/SidebarHeader.vue'
import SidebarTabs from './components/layout/SidebarTabs.vue'
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.app-main {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}
</style>

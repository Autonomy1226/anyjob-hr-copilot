<template>
  <el-alert :title="message" type="error" show-icon :closable="true" @close="$emit('close')" />
</template>

<script setup lang="ts">
defineProps<{ message: string }>()
defineEmits<{ close: [] }>()
</script>

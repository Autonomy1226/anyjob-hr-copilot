<template>
  <div class="skill-gap">
    <h4 class="section-title">技能匹配分析</h4>
    <div class="gap-list">
      <div v-for="skill in matchedSkills" :key="skill" class="gap-item match">
        <el-tag type="success" size="small" effect="plain">&#x2713; 匹配</el-tag>
        <span>{{ skill }}</span>
      </div>
      <div v-for="skill in missingSkills" :key="skill" class="gap-item miss">
        <el-tag type="danger" size="small" effect="plain">&#x2717; 缺失</el-tag>
        <span>{{ skill }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ matchedSkills: string[]; missingSkills: string[] }>()
</script>

<style scoped>
.skill-gap {
  background: var(--aj-surface);
  border: 1px solid var(--aj-border);
  border-radius: 8px;
  padding: 12px;
}
.section-title {
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 8px;
}
.gap-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.gap-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}
</style>

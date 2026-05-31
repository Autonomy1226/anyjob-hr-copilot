<template>
  <div class="matching-score">
    <div class="score-circle">
      <el-progress
        type="circle"
        :percentage="score"
        :color="scoreColor"
        :width="100"
      >
        <span class="score-value">{{ score }}</span>
      </el-progress>
    </div>
    <div class="score-info">
      <h3>综合匹配度</h3>
      <el-tag :type="recTagType" size="small">{{ recommendation }}</el-tag>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ score: number; recommendation: string }>()

const scoreColor = computed(() => {
  if (props.score >= 80) return '#10b981'
  if (props.score >= 60) return '#6366f1'
  if (props.score >= 40) return '#f59e0b'
  return '#ef4444'
})

const recTagType = computed(() => {
  if (props.recommendation.includes('强烈') || props.recommendation.includes('Strong')) return 'success'
  if (props.recommendation.includes('推荐') || props.recommendation.includes('Recommend')) return 'primary'
  if (props.recommendation.includes('考虑') || props.recommendation.includes('Consider')) return 'warning'
  return 'danger'
})
</script>

<style scoped>
.matching-score {
  display: flex;
  align-items: center;
  gap: 16px;
  background: var(--aj-surface);
  border: 1px solid var(--aj-border);
  border-radius: 8px;
  padding: 16px;
}
.score-circle {
  flex-shrink: 0;
}
.score-value {
  font-size: 24px;
  font-weight: 700;
}
.score-info h3 {
  font-size: 14px;
  margin-bottom: 4px;
}
</style>

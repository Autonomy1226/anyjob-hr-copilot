<template>
  <div class="matching-page">
    <template v-if="!store.parsed">
      <EmptyState text="请先在「简历解析」页面提取候选人信息" />
    </template>

    <template v-else>
      <div class="jd-section">
        <el-input
          v-model="jdText"
          type="textarea"
          :rows="4"
          placeholder="粘贴岗位 JD（岗位描述/任职要求）..."
        />
        <el-button
          type="primary"
          :loading="matchingLoading"
          :disabled="!jdText.trim()"
          @click="handleMatch"
          style="margin-top: 8px; width: 100%"
        >
          &#x1F3AF; 开始匹配
        </el-button>
      </div>

      <ErrorAlert v-if="store.error && store.matchingStatus === 'error'" :message="store.error" @close="store.error = null" />

      <LoadingSpinner v-if="matchingLoading" text="AI 正在评估匹配度..." />

      <template v-if="store.matchResult && store.matchingStatus === 'done'">
        <MatchingScore :score="store.matchResult.overall_score" :recommendation="store.matchResult.recommendation" />
        <RadarChart :dimensions="store.matchResult.radar_dimensions" />
        <SkillGapTable
          :matched-skills="store.matchResult.matched_skills"
          :missing-skills="store.matchResult.missing_skills"
        />
      </template>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useCandidateStore } from '@/stores/candidate.store'
import { useApi } from '@/composables/useApi'
import EmptyState from '@/components/shared/EmptyState.vue'
import ErrorAlert from '@/components/shared/ErrorAlert.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import MatchingScore from '@/components/matching/MatchingScore.vue'
import RadarChart from '@/components/matching/RadarChart.vue'
import SkillGapTable from '@/components/matching/SkillGapTable.vue'

const store = useCandidateStore()
const { matchCandidate } = useApi()
const jdText = ref('')

const matchingLoading = computed(() => store.matchingStatus === 'loading')

async function handleMatch() {
  if (!store.parsed || !jdText.value.trim()) return
  try {
    store.error = null
    store.matchingStatus = 'loading'
    const result = await matchCandidate(store.parsed, jdText.value.trim())
    store.setMatchResult(result)
  } catch (e) {
    store.setMatchingError((e as Error).message)
  }
}
</script>

<style scoped>
.matching-page {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.jd-section {
  background: var(--aj-surface);
  border: 1px solid var(--aj-border);
  border-radius: 8px;
  padding: 12px;
}
</style>

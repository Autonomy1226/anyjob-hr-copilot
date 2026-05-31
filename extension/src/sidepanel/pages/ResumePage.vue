<template>
  <div class="resume-page">
    <div class="page-actions">
      <el-button type="primary" :loading="loading" @click="handleExtract">
        &#x1F50D; 提取页面简历
      </el-button>
    </div>

    <ErrorAlert v-if="store.error && store.extractionStatus === 'error'" :message="store.error" @close="store.error = null" />

    <LoadingSpinner v-if="loading" text="AI 正在解析简历..." />

    <template v-if="store.parsed && store.extractionStatus === 'done' && !loading">
      <ResumeStructured :candidate="store.parsed" />
      <ResumeEditForm :candidate="store.parsed" />
    </template>

    <EmptyState v-if="store.extractionStatus === 'idle' && !store.parsed" text="点击上方按钮提取并解析当前页面的候选人简历" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useCandidateStore } from '@/stores/candidate.store'
import { useDomBridge } from '@/composables/useDomBridge'
import { useApi } from '@/composables/useApi'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import ErrorAlert from '@/components/shared/ErrorAlert.vue'
import EmptyState from '@/components/shared/EmptyState.vue'
import ResumeStructured from '@/components/resume/ResumeStructured.vue'
import ResumeEditForm from '@/components/resume/ResumeEditForm.vue'

const store = useCandidateStore()
const { getExtractedText } = useDomBridge()
const { parseResume } = useApi()

const loading = computed(() => store.extractionStatus === 'loading')

async function handleExtract() {
  try {
    store.error = null
    store.extractionStatus = 'loading'

    const { rawText, sourceSite } = await getExtractedText()
    store.setRawText(rawText, sourceSite)

    const result = await parseResume({ raw_text: rawText, source_site: sourceSite })
    store.setParsed(result)
  } catch (e) {
    store.setExtractionError((e as Error).message)
  }
}
</script>

<style scoped>
.resume-page {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.page-actions {
  display: flex;
  gap: 8px;
}
</style>

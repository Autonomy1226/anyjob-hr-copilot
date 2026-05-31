<template>
  <div class="message-page">
    <template v-if="!store.parsed">
      <EmptyState text="请先在「简历解析」页面提取候选人信息" />
    </template>

    <template v-else>
      <div class="template-section">
        <label class="field-label">消息类型</label>
        <el-radio-group v-model="templateType" size="small">
          <el-radio-button value="面试邀请">面试邀请</el-radio-button>
          <el-radio-button value="跟进">跟进</el-radio-button>
          <el-radio-button value="拒信">拒信</el-radio-button>
          <el-radio-button value="自定义">自定义</el-radio-button>
        </el-radio-group>
      </div>

      <div class="template-section" v-if="templateType === '自定义'">
        <label class="field-label">自定义指令</label>
        <el-input v-model="customInstruction" type="textarea" :rows="2" placeholder="描述你想要的沟通话术风格..." />
      </div>

      <el-button
        type="primary"
        :loading="genLoading"
        @click="handleGenerate"
        style="width: 100%"
      >
        &#x2728; 生成消息
      </el-button>

      <ErrorAlert v-if="store.error && store.messageStatus === 'error'" :message="store.error" @close="store.error = null" />

      <LoadingSpinner v-if="genLoading" text="AI 正在生成沟通话术..." />

      <div v-if="store.generatedMessage && store.messageStatus === 'done'" class="message-result">
        <div class="message-header">
          <span class="field-label">生成结果</span>
          <el-button size="small" text @click="handleCopy">复制到剪贴板</el-button>
        </div>
        <div class="message-body">{{ store.generatedMessage }}</div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useCandidateStore } from '@/stores/candidate.store'
import { useHistoryStore } from '@/stores/history.store'
import { useApi } from '@/composables/useApi'
import EmptyState from '@/components/shared/EmptyState.vue'
import ErrorAlert from '@/components/shared/ErrorAlert.vue'
import LoadingSpinner from '@/components/shared/LoadingSpinner.vue'
import { ElMessage } from 'element-plus'

const store = useCandidateStore()
const historyStore = useHistoryStore()
const { generateMessage } = useApi()

const templateType = ref<'面试邀请' | '拒信' | '跟进' | '自定义'>('面试邀请')
const customInstruction = ref('')

const genLoading = computed(() => store.messageStatus === 'loading')

async function handleGenerate() {
  if (!store.parsed) return
  try {
    store.error = null
    store.messageStatus = 'loading'
    const result = await generateMessage(
      store.parsed,
      store.parsed.current_title || '',
      store.parsed.current_company || '',
      templateType.value,
      customInstruction.value
    )
    store.setGeneratedMessage(result.message)
    historyStore.addMessage(result.message)
  } catch (e) {
    store.setMessageError((e as Error).message)
  }
}

async function handleCopy() {
  if (store.generatedMessage) {
    await navigator.clipboard.writeText(store.generatedMessage)
    ElMessage.success('已复制到剪贴板')
  }
}
</script>

<style scoped>
.message-page {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.template-section {
  background: var(--aj-surface);
  border: 1px solid var(--aj-border);
  border-radius: 8px;
  padding: 12px;
}
.field-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 8px;
}
.message-result {
  background: var(--aj-surface);
  border: 1px solid var(--aj-border);
  border-radius: 8px;
  padding: 12px;
}
.message-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.message-body {
  font-size: 13px;
  line-height: 1.6;
  white-space: pre-wrap;
  color: var(--aj-text);
  background: var(--aj-bg);
  padding: 10px;
  border-radius: 6px;
}
</style>

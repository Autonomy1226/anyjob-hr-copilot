<template>
  <div class="resume-structured">
    <el-descriptions :column="1" border size="small" title="候选人信息">
      <el-descriptions-item label="姓名">{{ candidate.name || '—' }}</el-descriptions-item>
      <el-descriptions-item label="当前职位">{{ candidate.current_title || '—' }}</el-descriptions-item>
      <el-descriptions-item label="当前公司">{{ candidate.current_company || '—' }}</el-descriptions-item>
      <el-descriptions-item label="工作年限">{{ candidate.years_of_experience ? candidate.years_of_experience + '年' : '—' }}</el-descriptions-item>
      <el-descriptions-item label="地点">{{ candidate.location || '—' }}</el-descriptions-item>
      <el-descriptions-item label="薪资期望">{{ candidate.salary_expectation || '—' }}</el-descriptions-item>
    </el-descriptions>

    <div v-if="candidate.skills.length" class="section">
      <h4 class="section-title">技能标签</h4>
      <div class="skill-tags">
        <el-tag v-for="skill in candidate.skills" :key="skill" size="small" type="info">
          {{ skill }}
        </el-tag>
      </div>
    </div>

    <div v-if="candidate.languages.length" class="section">
      <h4 class="section-title">语言能力</h4>
      <div class="skill-tags">
        <el-tag v-for="lang in candidate.languages" :key="lang" size="small" effect="plain">
          {{ lang }}
        </el-tag>
      </div>
    </div>

    <div v-if="candidate.education.length" class="section">
      <h4 class="section-title">教育背景</h4>
      <div v-for="(edu, idx) in candidate.education" :key="idx" class="edu-item">
        <span class="edu-school">{{ edu.school }}</span>
        <span class="edu-meta">{{ edu.degree }} · {{ edu.major }}
          <template v-if="edu.graduation_year"> · {{ edu.graduation_year }}届</template>
        </span>
      </div>
    </div>

    <div v-if="candidate.work_experience.length" class="section">
      <h4 class="section-title">工作经历</h4>
      <div v-for="(exp, idx) in candidate.work_experience" :key="idx" class="exp-item">
        <div class="exp-header">
          <strong>{{ exp.title }}</strong>
          <span class="exp-company">@ {{ exp.company }}</span>
          <span class="exp-duration">{{ Math.round(exp.duration_months / 12) }}年</span>
        </div>
        <p class="exp-desc">{{ exp.description }}</p>
        <div v-if="exp.skills_used.length" class="skill-tags">
          <el-tag v-for="s in exp.skills_used" :key="s" size="small">{{ s }}</el-tag>
        </div>
      </div>
    </div>

    <div v-if="candidate.summary" class="section">
      <h4 class="section-title">个人总结</h4>
      <p class="summary-text">{{ candidate.summary }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Candidate } from '@/types/candidate'

defineProps<{ candidate: Candidate }>()
</script>

<style scoped>
.resume-structured {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.section {
  background: var(--aj-surface);
  border: 1px solid var(--aj-border);
  border-radius: 8px;
  padding: 12px;
}
.section-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--aj-text);
  margin-bottom: 8px;
}
.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.edu-item, .exp-item {
  padding: 6px 0;
  border-bottom: 1px solid var(--aj-border);
}
.edu-item:last-child, .exp-item:last-child {
  border-bottom: none;
}
.edu-school {
  font-weight: 600;
}
.edu-meta {
  font-size: 12px;
  color: var(--aj-text-secondary);
  margin-left: 8px;
}
.exp-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
}
.exp-company {
  color: var(--aj-primary);
}
.exp-duration {
  font-size: 12px;
  color: var(--aj-text-secondary);
  margin-left: auto;
}
.exp-desc {
  margin: 4px 0;
  font-size: 12px;
  color: var(--aj-text-secondary);
}
.summary-text {
  font-size: 13px;
  line-height: 1.5;
  color: var(--aj-text-secondary);
}
</style>

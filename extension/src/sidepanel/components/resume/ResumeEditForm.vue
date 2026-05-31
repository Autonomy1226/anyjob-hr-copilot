<template>
  <el-collapse>
    <el-collapse-item title="编辑 / 补充信息" name="edit">
      <el-form :model="form" label-position="top" size="small">
        <el-form-item label="姓名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="当前职位">
          <el-input v-model="form.current_title" />
        </el-form-item>
        <el-form-item label="当前公司">
          <el-input v-model="form.current_company" />
        </el-form-item>
        <el-form-item label="工作年限">
          <el-input-number v-model="form.years_of_experience" :min="0" :max="50" />
        </el-form-item>
        <el-form-item label="技能 (逗号分隔)">
          <el-input v-model="skillsText" />
        </el-form-item>
        <el-form-item label="薪资期望">
          <el-input v-model="form.salary_expectation" />
        </el-form-item>
        <el-form-item label="地点">
          <el-input v-model="form.location" />
        </el-form-item>
        <el-button type="primary" size="small" @click="handleSave">保存修改</el-button>
      </el-form>
    </el-collapse-item>
  </el-collapse>
</template>

<script setup lang="ts">
import { reactive, ref, watch, computed } from 'vue'
import type { Candidate } from '@/types/candidate'

const props = defineProps<{ candidate: Candidate }>()

const form = reactive({
  name: '',
  current_title: '',
  current_company: '',
  years_of_experience: 0,
  salary_expectation: '',
  location: '',
})

const skillsText = ref('')

watch(
  () => props.candidate,
  (c) => {
    if (c) {
      form.name = c.name
      form.current_title = c.current_title
      form.current_company = c.current_company
      form.years_of_experience = c.years_of_experience
      form.salary_expectation = c.salary_expectation
      form.location = c.location
      skillsText.value = c.skills.join(', ')
    }
  },
  { immediate: true }
)

function handleSave() {
  props.candidate.name = form.name
  props.candidate.current_title = form.current_title
  props.candidate.current_company = form.current_company
  props.candidate.years_of_experience = form.years_of_experience
  props.candidate.skills = skillsText.value.split(',').map((s) => s.trim()).filter(Boolean)
  props.candidate.salary_expectation = form.salary_expectation
  props.candidate.location = form.location
  ElMessage.success('信息已更新')
}
</script>

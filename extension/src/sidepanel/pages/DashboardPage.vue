<template>
  <div class="dashboard-page">
    <div class="stat-grid">
      <StatCard title="今日解析简历" :value="stats.total_parsed" icon="📄" color="#6366f1" />
      <StatCard title="今日匹配评估" :value="stats.total_matched" icon="🎯" color="#10b981" />
      <StatCard title="生成消息数" :value="stats.total_messages" icon="💬" color="#f59e0b" />
      <StatCard title="平均匹配度" :value="stats.avg_match_score + '%'" icon="⭐" color="#ef4444" />
    </div>

    <div class="chart-section">
      <h4 class="section-title">每日活动趋势</h4>
      <v-chart :option="chartOption" autoresize style="height: 200px" />
    </div>

    <div class="activity-section">
      <h4 class="section-title">最近活动</h4>
      <el-timeline v-if="stats.recent_activity?.length">
        <el-timeline-item
          v-for="(item, idx) in stats.recent_activity"
          :key="idx"
          :timestamp="item.timestamp"
          placement="top"
          size="small"
        >
          <strong>{{ item.action }}</strong>
          <span v-if="item.candidate_name"> — {{ item.candidate_name }}</span>
          <p v-if="item.detail" class="activity-detail">{{ item.detail }}</p>
        </el-timeline-item>
      </el-timeline>
      <EmptyState v-else text="暂无活动记录" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { useApi } from '@/composables/useApi'
import type { DashboardStats } from '@/types/api'
import StatCard from '@/components/dashboard/StatCard.vue'
import EmptyState from '@/components/shared/EmptyState.vue'

use([BarChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent, CanvasRenderer])

const { getDashboardStats } = useApi()

const stats = ref<DashboardStats>({
  total_parsed: 0,
  total_matched: 0,
  total_messages: 0,
  avg_match_score: 0,
  daily_breakdown: [],
  recent_activity: [],
})

const chartOption = computed(() => ({
  tooltip: { trigger: 'axis' as const },
  grid: { top: 10, bottom: 20, left: 40, right: 10 },
  xAxis: {
    type: 'category' as const,
    data: stats.value.daily_breakdown.map((d) => d.date.slice(5)),
    axisLabel: { fontSize: 10 },
  },
  yAxis: {
    type: 'value' as const,
    minInterval: 1,
    axisLabel: { fontSize: 10 },
  },
  series: [
    { name: '解析', type: 'bar', data: stats.value.daily_breakdown.map((d) => d.parsed_count), itemStyle: { color: '#6366f1' } },
    { name: '匹配', type: 'bar', data: stats.value.daily_breakdown.map((d) => d.matched_count), itemStyle: { color: '#10b981' } },
    { name: '消息', type: 'bar', data: stats.value.daily_breakdown.map((d) => d.message_count), itemStyle: { color: '#f59e0b' } },
  ],
}))

onMounted(async () => {
  try {
    stats.value = await getDashboardStats(7)
  } catch {
    // Use empty stats as fallback
  }
})
</script>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.stat-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.chart-section, .activity-section {
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
.activity-detail {
  font-size: 12px;
  color: var(--aj-text-secondary);
}
</style>

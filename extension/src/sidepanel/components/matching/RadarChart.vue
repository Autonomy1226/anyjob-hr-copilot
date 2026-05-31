<template>
  <div class="radar-chart-container">
    <h4 class="chart-title">能力雷达图</h4>
    <v-chart :option="chartOption" autoresize style="height: 280px" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { RadarChart as ERadar } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import type { RadarDimension } from '@/types/matching'

use([ERadar, TitleComponent, TooltipComponent, LegendComponent, GridComponent, CanvasRenderer])

const props = defineProps<{ dimensions: RadarDimension[] }>()

const chartOption = computed(() => ({
  tooltip: {
    trigger: 'item' as const,
  },
  legend: {
    data: ['候选人', '岗位要求'],
    bottom: 0,
    textStyle: { fontSize: 11 },
  },
  radar: {
    center: ['50%', '50%'],
    radius: '65%',
    indicator: props.dimensions.map((d) => ({
      name: d.name,
      max: 100,
    })),
    axisName: {
      fontSize: 10,
    },
  },
  series: [
    {
      type: 'radar' as const,
      data: [
        {
          name: '候选人',
          value: props.dimensions.map((d) => d.score),
          areaStyle: { color: 'rgba(99, 102, 241, 0.15)' },
          lineStyle: { color: '#6366f1', width: 2 },
          itemStyle: { color: '#6366f1' },
        },
        {
          name: '岗位要求',
          value: props.dimensions.map(() => 70), // baseline JD requirement
          areaStyle: { color: 'rgba(100, 116, 139, 0.08)' },
          lineStyle: { color: '#94a3b8', width: 2, type: 'dashed' as const },
          itemStyle: { color: '#94a3b8' },
        },
      ],
    },
  ],
}))
</script>

<style scoped>
.radar-chart-container {
  background: var(--aj-surface);
  border: 1px solid var(--aj-border);
  border-radius: 8px;
  padding: 12px;
}
.chart-title {
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 8px;
}
</style>

<template>
  <div class="dashboard-view" v-loading="loading">
    <!-- 顶部 4 个数据卡片 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-title">工单总数</div>
          <div class="stat-value">{{ stats.total }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-title">待处理</div>
          <div class="stat-value warning">{{ stats.pending }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-title">已解决/关闭</div>
          <div class="stat-value success">{{ stats.resolved }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card ai-card">
          <div class="stat-title">AI 分类准确率</div>
          <div class="stat-value primary">{{ stats.ai_accuracy }}%</div>
          <div class="stat-desc">基于用户是否手动修改分类计算</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>工单分类分布</template>
          <div ref="pieChartRef" style="height: 320px;"></div>
          <el-empty v-if="stats.category_data.length === 0" description="暂无数据" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>系统简介</template>
          <div class="intro-content">
            <h3>AI-Powered Ticket Hub</h3>
            <p>本系统融合了大语言模型（LLM）与向量检索（RAG），旨在解决企业内部 IT 支持中“重复问题反复处理、经验无法沉淀”的痛点。</p>
            <ul>
              <li>✅ 智能分类与摘要</li>
              <li>✅ 状态机驱动的工单流转</li>
              <li>✅ 向量语义检索与知识沉淀</li>
              <li>✅ 基于 SSE 的流式 AI 问答</li>
            </ul>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import request from '@/api/request'

const loading = ref(false)
const stats = ref({
  total: 0,
  pending: 0,
  resolved: 0,
  ai_accuracy: 0,
  category_data: [] as { name: string; value: number }[]
})

const pieChartRef = ref<HTMLElement>()

async function loadStats() {
  loading.value = true
  try {
    const res = await request.get('/stats/overview')
    stats.value = res
    // 数据加载完成后，渲染图表
    nextTick(() => {
      renderPie()
    })
  } catch (e) {
    // 拦截器已处理
  } finally {
    loading.value = false
  }
}

function renderPie() {
  if (!pieChartRef.value || stats.value.category_data.length === 0) return
  const chart = echarts.init(pieChartRef.value)
  chart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: '0%' },
    series: [
      {
        name: '工单分类',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: { show: false },
        data: stats.value.category_data
      }
    ]
  })

  // 响应式自适应
  window.addEventListener('resize', () => chart.resize())
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.dashboard-view {
  padding: 0;
}

.stat-card {
  text-align: center;
  padding: 10px;
  border-radius: 8px;
}
.stat-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 12px;
}
.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
}
.stat-value.warning { color: #E6A23C; }
.stat-value.success { color: #67C23A; }
.stat-value.primary { color: #409EFF; }

.stat-desc {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}

.ai-card {
  background: linear-gradient(135deg, #f0f9eb 0%, #e1f3d8 100%);
  border: 1px solid #c2e7b0;
}

.chart-row {
  margin-top: 20px;
}

.intro-content {
  padding: 10px;
  color: #606266;
  line-height: 1.8;
}
.intro-content h3 {
  margin-top: 0;
  color: #303133;
}
.intro-content ul {
  padding-left: 20px;
}
</style>
<template>
  <el-card class="ai-panel" shadow="never">
    <template #header>
      <div class="panel-header">
        <span class="title">
          <el-icon><MagicStick /></el-icon>
          AI 智能分析
        </span>
        <el-tag v-if="loading" type="info" size="small">分析中...</el-tag>
      </div>
    </template>

    <!-- 空状态：还没输入 -->
    <el-empty
      v-if="!hasInput && !loading"
      description="输入标题和描述后，AI 会自动分析"
      :image-size="80"
    />

    <!-- 有结果 -->
    <div v-else-if="result" class="result-block">
      <!-- 分类 -->
      <div class="field">
        <div class="field-label">建议分类</div>
        <div class="field-value">
          <el-tag type="success">{{ result.category }}</el-tag>
          <el-button
            link
            size="small"
            @click="emit('correct-category')"
          >
            修改
          </el-button>
        </div>
      </div>

      <!-- 优先级 -->
      <div class="field">
        <div class="field-label">建议优先级</div>
        <div class="field-value">
          <StatusTag :value="result.priority" type="priority" />
        </div>
      </div>

      <!-- 置信度 -->
      <div class="field">
        <div class="field-label">AI 置信度</div>
        <el-progress
          :percentage="Math.round(result.confidence * 100)"
          :stroke-width="8"
          :color="confidenceColor"
        />
      </div>

      <!-- 摘要 -->
      <div class="field">
        <div class="field-label">AI 摘要</div>
        <div class="summary-text">{{ result.summary }}</div>
      </div>
    </div>

    <!-- 分析中 -->
    <div v-else-if="loading" class="loading-block">
      <el-skeleton :rows="4" animated />
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import StatusTag from '../common/StatusTag.vue';
import type { AIAnalysisResult } from '@/api/ai'; 

const props=defineProps<{
    loading:boolean,
    result:AIAnalysisResult | null,
    hasInput:boolean
}>()

const emit=defineEmits<{
    (e:"correct-category"):void
}>()

const confidenceColor=computed(()=>{
    const c = props.result?.confidence ?? 0
    if(c>=0.8) return '#67c23a'
    if(c>=0.5) return '#e6a23c'
    return '#f56c6c'
})
</script>

<style scoped>
.ai-panel {
  height: 100%;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
}

.result-block {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label {
  font-size: 13px;
  color: #999;
}

.field-value {
  display: flex;
  align-items: center;
  gap: 8px;
}

.summary-text {
  font-size: 14px;
  color: #333;
  line-height: 1.6;
  padding: 8px 12px;
  background: #f5f7fa;
  border-radius: 4px;
}

.loading-block {
  padding: 8px 0;
}
</style>
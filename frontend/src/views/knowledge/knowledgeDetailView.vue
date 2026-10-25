<template>
  <div v-loading="loading" class="detail-view">
    <el-page-header @back="router.back()" class="page-header">
      <template #content>
        <span>知识详情</span>
      </template>
    </el-page-header>

    <el-card v-if="knowledge" shadow="never" class="content-card">
      <h1 class="title">{{ knowledge.title }}</h1>
      
      <div class="meta">
        <span>发布时间：{{ formatTime(knowledge.created_at) }}</span>
        <el-tag v-if="knowledge.source_ticket_id" size="small" type="info" class="source-tag">
          来源工单：#{{ knowledge.source_ticket_id }}
        </el-tag>
      </div>

      <el-divider />

      <div class="content">
        <!-- 用 pre-wrap 保留换行格式 -->
        {{ knowledge.content }}
      </div>
    </el-card>
  </div>
</template>
<script setup lang="ts">
import {onMounted,ref} from 'vue'
import {useRouter,useRoute} from 'vue-router'
import { type Knowledge,getKnowledgeDetail } from '@/api/knowledge'
import {formatTime} from '@/utils/format'

const router = useRouter()
const route=useRoute()
const loading = ref(false)
const knowledge = ref<Knowledge | null>(null)

const loadData=async()=>{
    loading.value=true
    try {
        knowledge.value=await getKnowledgeDetail(Number(route.params.id))
    } catch (error) {
        
    }finally{
        loading.value=false
    }
}
onMounted(loadData)

</script>
<style scoped>
.detail-view {
  padding: 0;
}

.page-header {
  margin-bottom: 16px;
}

.content-card {
  padding: 10px;
}

.title {
  margin-top: 0;
  font-size: 24px;
  color: #303133;
}

.meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  color: #909399;
  margin-top: 12px;
}

.content {
  font-size: 15px;
  line-height: 1.8;
  color: #303133;
  white-space: pre-wrap;  /* 保留换行 */
}
</style>
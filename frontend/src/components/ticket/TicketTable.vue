<template>
  <el-table
    :data="tickets"
    stripe
    style="width: 100%"
    @row-click="handleRowClick"
  >
    <el-table-column prop="id" label="ID" width="80" />

    <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip>
      <template #default="{ row }">
        <div class="title-cell">
          <span>{{ row.title }}</span>
          <el-tooltip
            v-if="row.ai_summary"
            :content="row.ai_summary"
            placement="top"
          >
            <el-tag type="success" size="small" effect="plain">
              <el-icon><MagicStick /></el-icon>
              AI
            </el-tag>
          </el-tooltip>
        </div>
      </template>
    </el-table-column>

    <el-table-column label="分类" width="120">
      <template #default="{ row }">
        <span>{{ row.category || '-' }}</span>
      </template>
    </el-table-column>

    <el-table-column label="优先级" width="100">
      <template #default="{ row }">
        <StatusTag :value="row.priority" type="priority" />
      </template>
    </el-table-column>

    <el-table-column label="状态" width="100">
      <template #default="{ row }">
        <StatusTag :value="row.status" />
      </template>
    </el-table-column>

    <el-table-column label="创建人" width="120">
      <template #default="{ row }">
        {{ row.creator_username }}
      </template>
    </el-table-column>

    <el-table-column label="处理人" width="120">
      <template #default="{ row }">
        {{ row.assignee_username || '未分配' }}
      </template>
    </el-table-column>

    <el-table-column label="创建时间" width="180">
      <template #default="{ row }">
        {{ formatTime(row.created_at) }}
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';
import StatusTag from '@/components/common/StatusTag.vue'
import {formatTime} from '@/utils/format'
import type {Ticket} from '@/api/ticket'

defineProps<{tickets:Ticket[]}>()

const router = useRouter()
const handleRowClick = (row:Ticket)=>{
    router.push(`/tickets/${row.id}`)
}
</script>

<style scoped>
.title-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.el-table__row) {
  cursor: pointer;
}
</style>
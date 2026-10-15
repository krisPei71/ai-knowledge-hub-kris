<template>
  <el-timeline>
    <el-timeline-item
      v-for="log in logs"
      :key="log.id"
      :timestamp="formatTime(log.created_at)"
      :type="getTimelineType(log.to_status)"
      placement="top"
    >
      <div class="timeline-content">
        <div class="timeline-main">
          <strong>{{ log.operator_username }}</strong>
          <template v-if="log.from_status">
            将状态从
            <StatusTag :value="log.from_status" />
          </template>
          <template v-else> 创建工单，初始状态 </template>
          改为
          <StatusTag :value="log.to_status" />
        </div>
        <div v-if="log.remark" class="timeline-remark">
          备注：{{ log.remark }}
        </div>
      </div>
    </el-timeline-item>

    <el-empty v-if="!logs.length" description="暂无流转记录" />
  </el-timeline>
</template>

<script lang="ts" setup>
import StatusTag from "@/components/common/StatusTag.vue";
import { formatTime } from "@/utils/format";
import type { TicketLog } from "@/api/ticket";

defineProps<{ logs: TicketLog }>();

const getTimelineType = (status: string) => {
  const map:Record<string,'primary' | 'success' | 'warning' | 'info' | 'danger'> = {
    pending: "info",
    processing: "primary",
    resolved: "success",
    closed: "warning",
  };
  return map[status] || "info";
};
</script>

<style scoped>
.timeline-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.timeline-main {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  color: #333;
}

.timeline-remark {
  font-size: 13px;
  color: #666;
  background: #f5f7fa;
  padding: 6px 10px;
  border-radius: 4px;
  margin-top: 4px;
}
</style>

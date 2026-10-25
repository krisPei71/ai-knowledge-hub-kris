<template>
  <div v-loading="loading" class="detail-view">
    <!-- 顶部：标题 + 状态标签 -->
    <el-card shadow="never" class="header-card">
      <div class="header-row">
        <div class="title-area">
          <span class="ticket-id">#{{ ticket?.id }}</span>
          <h2>{{ ticket?.title }}</h2>
        </div>
        <div class="tags-area">
          <StatusTag v-if="ticket" :value="ticket.priority" type="priority" />
          <StatusTag v-if="ticket" :value="ticket.status" />
        </div>
      </div>
      <!-- D2-5 会在这里加状态流转按钮组 -->
      <div class="actions-area">
        <el-button
          v-for="t in availableTransitions"
          :key="t.to"
          :type="t.type"
          @click="handleTransition(t)"
        >
          {{ t.label }}
        </el-button>

        <el-button
          v-if="ticket?.status === 'resolved' || ticket?.status === 'closed'"
          type="warning"
          plain
          @click="handleToKnowledge"
        >
          <el-icon><Collection /></el-icon> 一键沉淀为知识库
        </el-button>
      </div>
    </el-card>

    <el-row :gutter="16">
      <!-- 左侧主区 -->
      <el-col :span="16">
        <el-card shadow="never" class="info-card">
          <template #header>
            <span>工单信息</span>
          </template>

          <el-descriptions :column="2" border>
            <el-descriptions-item label="创建人">
              {{ ticket?.creator_username || "-" }}
            </el-descriptions-item>
            <el-descriptions-item label="处理人">
              {{ ticket?.assignee_username || "未分配" }}
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">
              {{ formatTime(ticket?.created_at) }}
            </el-descriptions-item>
            <el-descriptions-item label="更新时间">
              {{ formatTime(ticket?.updated_at) }}
            </el-descriptions-item>
            <el-descriptions-item label="分类">
              {{ ticket?.category || "未分类" }}
            </el-descriptions-item>
            <el-descriptions-item label="AI 置信度">
              <span v-if="ticket?.ai_confidence">
                {{ (ticket.ai_confidence * 100).toFixed(1) }}%
              </span>
              <span v-else>-</span>
            </el-descriptions-item>
          </el-descriptions>

          <div class="description-block">
            <div class="block-label">问题描述</div>
            <div class="block-content">{{ ticket?.description }}</div>
          </div>

          <!-- D3 会在这里加 AI 摘要卡 -->
        </el-card>

        <!-- 状态时间线 -->
        <el-card shadow="never" class="timeline-card">
          <template #header>
            <span>流转记录</span>
          </template>
          <TicketTimeline :logs="logs" />
        </el-card>
      </el-col>

      <!-- 右侧侧栏 -->
      <el-col :span="8">
        <el-card shadow="never" class="side-card">
          <template #header>
            <span>相似工单</span>
          </template>
          <!-- D3 填 -->
          <el-empty description="D3 实现" :image-size="80" />
        </el-card>

        <el-card shadow="never" class="side-card">
          <template #header>
            <span>知识库匹配</span>
          </template>
          <!-- D4 填 -->
          <el-empty description="D4 实现" :image-size="80" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { formatTime } from "@/utils/format";
import {
  getTicketDetail,
  getTicketLogs,
  updateTicketStatus,
  type Ticket,
  type TicketLog,
} from "@/api/ticket";
import { useUserStore } from "@/stores/user.ts";
import { useRoute } from "vue-router";
import TicketTimeline from "./TicketTimeline.vue";
import StatusTag from "@/components/common/StatusTag.vue";
import {
  getAvailableTransition,
  type Transition,
} from "@/utils/statusMachine.ts";
import { ElMessage, ElMessageBox } from "element-plus";
import { ticketToKnowledge } from '@/api/ticket'
import { Collection } from '@element-plus/icons-vue'

const useStore = useUserStore();
const route = useRoute();
const ticketId = Number(route.params.id);
const loading = ref(false);
const ticket = ref<Ticket | null>(null);
const logs = ref<TicketLog[]>([]);

const availableTransitions = computed(() => {
  if (!ticket.value) return [];
  return getAvailableTransition(ticket.value, useStore.userInfo);
});

const handleTransition = async (t: Transition) => {
  let remark: string | null = null;

  // 需要备注时弹输入框
  if (t.remarkRequired) {
    const result = await ElMessageBox.prompt(
      "请输入操作备注（必填）",
      t.label,
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPlaceholder: "说明原因...",
        inputValidator: (val) => !!val?.trim() || "备注不能为空",
      }
    ).catch(() => null);

    if (!result) return; // 用户取消
    remark = result.value;
  } else {
    // 不需要备注，二次确认
    const confirmed = await ElMessageBox.confirm(
      `确定要执行「${t.label}」吗？`,
      "确认操作",
      { confirmButtonText: "确定", cancelButtonText: "取消", type: "warning" }
    ).catch(() => false);

    if (!confirmed) return;
  }

  try {
    await updateTicketStatus(ticketId, { to_status: t.to, remark });
    ElMessage.success("操作成功");
    await loadData();
  } catch (error) {}
};
const loadData = async () => {
  loading.value = true;
  try {
    const [t, l] = await Promise.all([
      getTicketDetail(ticketId),
      getTicketLogs(ticketId),
    ]);
    ticket.value = t;
    logs.value = l;
  } catch (error) {
  } finally {
    loading.value = false;
  }
};

onMounted(loadData);

const handleToKnowledge=async ()=>{
  const result = await ElMessageBox.prompt(
    '请简述本次问题的解决方案（如果留空，将自动使用解决时填写的备注）',
    '沉淀为知识库',
    {
      confirmButtonText: '确认沉淀',
      cancelButtonText: '取消',
      inputType: 'textarea',
      inputPlaceholder: '例如：清除浏览器缓存后重新登录即可',
    }
  ).catch(() => null)

  if (!result) return 

  try {
    await ticketToKnowledge(ticketId,{solution:result.value})
    ElMessage.success("沉淀知识库成功")
  } catch (error) {
    
  }
}
</script>

<style scoped>
.detail-view {
  padding: 0;
}

.header-card {
  margin-bottom: 16px;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.title-area {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-area h2 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.ticket-id {
  color: #999;
  font-size: 14px;
}

.tags-area {
  display: flex;
  gap: 8px;
  align-items: center;
}

.info-card,
.timeline-card {
  margin-bottom: 16px;
}

.description-block {
  margin-top: 16px;
}

.block-label {
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
}

.block-content {
  padding: 12px;
  background: #fafafa;
  border-radius: 4px;
  line-height: 1.7;
  color: #333;
  white-space: pre-wrap; /* 保留换行 */
}

.side-card {
  margin-bottom: 16px;
}

.actions-area {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}
</style>
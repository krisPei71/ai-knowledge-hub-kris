<template>
  <div class="chat-container">
    <div class="chat-history" ref="historyRef">
      <!-- 用户的消息 -->
      <!-- <div v-if="userQuery" class="message user">
        <el-avatar :size="32">U</el-avatar>
        <div class="bubble">{{ userQuery }}</div>
      </div> -->

      <!-- AI 的回答 -->
      <!-- <div v-if="aiAnswer || sources.length > 0" class="message ai">
        <el-avatar :size="32" type="primary">AI</el-avatar>
        <div class="bubble-wrap"> -->
      <!-- 引用来源 -->
      <!-- <div v-if="sources.length > 0" class="sources">
            <div class="sources-title">参考来源：</div>
            <el-tag
              v-for="s in sources"
              :key="s.id"
              class="source-tag"
              @click="goToKnowledge(s.id)"
            >
              📄 {{ s.title }}
            </el-tag>
          </div> -->

      <!-- AI 打字机文本 -->
      <!-- <div class="bubble">
            {{ aiAnswer }}<span v-if="loading" class="cursor">|</span>
          </div>
        </div>
      </div>
    </div> -->
      <!-- 👈 遍历所有消息 -->
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message', msg.role]"
      >
        <el-avatar :size="32" :type="msg.role === 'assistant' ? 'primary' : ''">
          {{ msg.role === "user" ? "U" : "AI" }}
        </el-avatar>

        <div class="bubble-wrap">
          <!-- 来源展示 -->
          <div v-if="msg.sources && msg.sources.length > 0" class="sources">
            <div class="sources-title">参考来源：</div>
            <el-tag
              v-for="s in msg.sources"
              :key="s.id"
              class="source-tag"
              @click="goToKnowledge(s.id)"
            >
              📄 {{ s.title }}
            </el-tag>
          </div>

          <!-- 文本展示 -->
          <div class="bubble">
            {{ msg.content }}
            <!-- 光标：只有当它在打字（loading）并且是最后一条消息时才显示 -->
            <span
              v-if="
                loading &&
                index === messages.length - 1 &&
                msg.role === 'assistant'
              "
              class="cursor"
              >|</span
            >
          </div>
        </div>
      </div>
    </div>
    <!-- 输入框 -->
    <div class="chat-input-area">
      <el-input
        v-model="inputText"
        type="textarea"
        :rows="2"
        placeholder="请提问，AI 将检索知识库回答您..."
        @keyup.enter.prevent="handleSend"
      />
      <el-button type="primary" :loading="loading" @click="handleSend">
        发送
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from "vue";
import { useRouter } from "vue-router";
import { streamChat, type ChatSource } from "@/api/ai";

const router = useRouter();
const inputText = ref("");
const userQuery = ref("");
const aiAnswer = ref("");
const sources = ref<ChatSource[]>([]);
const loading = ref(false);
const historyRef = ref<HTMLElement>();

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: ChatSource[];
}
const messages = ref<Message[]>([]);
async function handleSend() {
  const q = inputText.value.trim();
  if (!q || loading.value) return;

  messages.value.push({ role: "user", content: q });
  inputText.value = "";
  loading.value = true;
  scrollToBottom();

  const aiMsgIndex =
    messages.value.push({ role: "assistant", content: "", sources: [] }) - 1;
  const aiMsg = messages.value[aiMsgIndex];

  const historyPayload = messages.value.slice(0, -2).map((m) => ({
    role: m.role,
    content: m.content,
  }));

  // 初始化状态
  //   userQuery.value = q;
  //   aiAnswer.value = "";
  //   sources.value = [];
  //   loading.value = true;
  //   inputText.value = "";

  try {
    await streamChat(q, historyPayload, (chunk) => {
      if (chunk.type === "source") {
        aiMsg.sources = chunk.data; // ✅ 写到 aiMsg
      } else if (chunk.type === "text") {
        aiMsg.content += chunk.data; // ✅ 拼字到 aiMsg.content
        scrollToBottom();
      } else if (chunk.type === "done") {
        loading.value = false;
      }
    });
  } catch (e) {
    aiMsg.content = "抱歉，网络出了点问题。";
    loading.value = false;
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (historyRef.value) {
      historyRef.value.scrollTop = historyRef.value.scrollHeight;
    }
  });
}

function goToKnowledge(id: number) {
  router.push(`/knowledge/${id}`);
}
</script>

<style scoped>
/* 整个聊天页面：铺满高度，纵向排列 */
.chat-container {
  display: flex;
  flex-direction: column; /* 从上到下排列：消息区在上，输入框在下 */
  height: calc(100vh - 120px); /* 减去顶部导航栏的高度（根据你实际布局微调） */
  background: #fff;
  border-radius: 8px;
  overflow: hidden; /* 防止超出屏幕 */
}

/* 消息列表区：占据所有剩余空间，且可以滚动 */
.chat-history {
  flex: 1; /* 核心：自动撑满剩余高度 */
  padding: 20px;
  overflow-y: auto; /* 核心：内容多了出现滚动条 */
  display: flex;
  flex-direction: column; /* 让消息从上往下排 */
}

/* 消息气泡容器 */
.message {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.message.user {
  flex-direction: row-reverse; /* 用户的消息靠右 */
}

.bubble-wrap {
  max-width: 80%;
}

/* 气泡文字样式 */
.bubble {
  background: #f4f4f5;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word; /* 防止长英文或 URL 撑破气泡 */
}

.message.user .bubble {
  background: #409eff;
  color: white;
}

/* 来源标签 */
.sources {
  margin-bottom: 8px;
}
.sources-title {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}
.source-tag {
  margin-right: 8px;
  cursor: pointer;
  margin-bottom: 4px;
}

/* 光标闪烁动画 */
.cursor {
  display: inline-block;
  width: 2px;
  height: 14px;
  background: #333;
  vertical-align: middle;
  margin-left: 2px;
  animation: blink 1s step-end infinite;
}
@keyframes blink {
  50% {
    opacity: 0;
  }
}

/* 底部输入框：固定在底部 */
.chat-input-area {
  padding: 16px;
  border-top: 1px solid #ebeef5;
  display: flex;
  gap: 12px;
  background: #fafafa;
  flex-shrink: 0; /* 核心：告诉浏览器，不管消息再多，这个输入框不允许被压缩 */
}
</style>
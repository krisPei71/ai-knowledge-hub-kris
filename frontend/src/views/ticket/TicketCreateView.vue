<template>
  <div class="create-view">
    <el-page-header @back="router.back()">
      <template #content>
        <span>创建工单</span>
      </template>
    </el-page-header>

    <el-row :gutter="16" class="content-row">
      <!-- 左：表单 -->
      <el-col :span="14">
        <el-card shadow="never">
          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            label-position="top"
          >
            <el-form-item label="标题" prop="title">
              <el-input
                v-model="form.title"
                placeholder="一句话描述问题，例如：VPN连不上"
                maxlength="200"
                show-word-limit
              />
            </el-form-item>

            <el-form-item label="详细描述" prop="description">
              <el-input
                v-model="form.description"
                type="textarea"
                :rows="8"
                placeholder="详细描述问题现象、发生时间、影响范围..."
                maxlength="2000"
                show-word-limit
              />
            </el-form-item>

            <el-form-item label="分类" prop="category">
              <el-select
                v-model="form.category"
                placeholder="可留空，由 AI 自动判断"
                clearable
                style="width: 100%"
              >
                <el-option
                  v-for="c in CATEGORY_OPTIONS"
                  :key="c"
                  :label="c"
                  :value="c"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="优先级" prop="priority">
              <el-radio-group v-model="form.priority">
                <el-radio-button value="low">低</el-radio-button>
                <el-radio-button value="medium">中</el-radio-button>
                <el-radio-button value="high">高</el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                :loading="submitting"
                @click="handleSubmit"
              >
                提交工单
              </el-button>
              <el-button @click="router.back()">取消</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 右：AI 面板 -->
      <el-col :span="10">
        <AiPanel
          :result="aiResult"
          :loading="aiLoading"
          :has-input="hasInput"
          @correct-category="focusCategoryField"
        />
      </el-col>
    </el-row>
  </div>
</template>
<script setup lang="ts">
import { useRouter } from "vue-router";
import { ref, reactive, computed } from "vue";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";
import AiPanel from "@/components/ai/AiPanel.vue";
import { useDebounce } from "@/composables/useDebounce";
import { createTicket } from "@/api/ticket";
import { classifyTicket, type AIAnalysisResult } from "@/api/ai";

const router = useRouter();

const formRef = ref<FormInstance>();
const form = reactive({
  title: "",
  description: "",
  category: "", // 用户最终选定的分类
  priority: "medium" as "low" | "medium" | "high",
});
const rules: FormRules = {
  title: [{ required: true, message: "请输入标题", trigger: "blur" }],
  description: [{ required: true, message: "请输入描述", trigger: "blur" }],
};
const CATEGORY_OPTIONS = ["网络", "硬件", "软件", "账号权限", "邮箱", "其他"];

const submitting = ref(false);

const aiResult = ref<AIAnalysisResult | null>(null);
const aiLoading = ref(false);
const aiRawCategory = ref<string>("");

const hasInput = computed(() => {
  return form.title.trim().length > 0 || form.description.trim().length > 0;
});
const inputText = computed(() => {
  return `${form.title}|||${form.description}`;
});
const focusCategoryField = () => {
  ElMessage.info('请在上方"分类"下拉框中手动选择');
};

useDebounce(
  inputText,
  async () => {
    if (!hasInput.value) {
      aiResult.value = null;
      return;
    }
    aiLoading.value = true;
    try {
      const result = await classifyTicket({
        title: form.title,
        description: form.description,
      });
      aiResult.value = result;
      aiRawCategory.value = result.category;

      if (!form.category) {
        form.category = result.category;
      }
    } catch (error) {
      aiResult.value = null;
    } finally {
      aiLoading.value = false;
    }
  },
  800
);
const handleSubmit = () => {
  formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true;
      try {
        const payload = {
          title: form.title,
          description: form.description,
          category: form.category || null,
          priority: form.priority,
          ai_category_raw: aiRawCategory.value || null,
          ai_confidence: aiResult.value?.confidence ?? null,
          ai_summary: aiResult.value?.summary ?? null,
        };
        await createTicket(payload);
        ElMessage.success("创建成功");
        router.push("/tickets");
      } catch (error) {
      } finally {
        submitting.value = false;
      }
    }
  });
};
</script>
<style scoped>
.create-view {
  padding: 0;
}

.content-row {
  margin-top: 16px;
}
</style>
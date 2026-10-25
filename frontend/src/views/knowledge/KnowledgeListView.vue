<template>
  <div class="knowledge-view">
    <el-card shadow="never">
      <!-- 搜索区 -->
      <div class="search-header">
        <div class="search-box">
          <el-input
            v-model="searchQuery"
            placeholder="输入描述，AI 为您寻找相关知识（如：连不上内网怎么办）"
            size="large"
            clearable
            @keyup.enter="handleSearch"
            @clear="resetSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
            <template #append>
              <el-button @click="handleSearch" :loading="loading">
                语义搜索
              </el-button>
            </template>
          </el-input>
        </div>
        <div v-if="isSearching" class="search-tip">
          正在展示语义搜索的结果，按相似度排序
          <el-button link type="primary" @click="resetSearch"
            >返回全部列表</el-button
          >
        </div>
      </div>

      <!-- 列表区 -->
      <div v-loading="loading" class="list-container">
        <el-empty
          v-if="displayList.length === 0"
          description="暂无知识库内容"
        />

        <div
          v-for="item in displayList"
          :key="item.id"
          class="knowledge-card"
          @click="goToDetail(item.id)"
        >
          <div class="card-main">
            <h3 class="title">{{ item.title }}</h3>
            <p class="snippet">{{ item.content }}</p>
          </div>

          <!-- 如果是搜索状态，显示相似度分数 -->
          <div v-if="isSearching" class="score-badge">
            <el-tag :type="getScoreType(item.score)" effect="dark" round>
              相似度 {{ (item.score * 100).toFixed(1) }}%
            </el-tag>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import {
  type Knowledge,
  type KnowledgeSearchResult,
  getKnowledgeList,
  searchKnowledge,
} from "@/api/knowledge";

const router = useRouter();
const searchQuery = ref('');
const isSearching = ref(false);
const loading = ref(false);
const allKnowledge = ref<Knowledge[]>([]);
const knowledgeSearch = ref<KnowledgeSearchResult[]>([]);

const displayList = computed(() => {
  return isSearching.value ? knowledgeSearch.value : allKnowledge.value;
});

const loadAll = async () => {
  loading.value = true;
  try {
    allKnowledge.value = await getKnowledgeList();
    console.log(allKnowledge.value,888);
    console.log(displayList.value,99)
  } catch (error) {
  } finally {
    loading.value = false;
  }
};

onMounted(()=>{
    loadAll()
});
const resetSearch = () => {
  searchQuery.value = "";
  isSearching.value = false;
  knowledgeSearch.value = [];
};
const handleSearch = async () => {
  const q = searchQuery.value.trim();
  if (!q) {
    resetSearch();
    return;
  }
  loading.value = true;
  isSearching.value = true;
  try {
    knowledgeSearch.value = await searchKnowledge({ query: q, top_k: 5 });
  } catch (error) {
    isSearching.value = false;
  } finally {
    loading.value = false;
  }
};
const goToDetail = (id: number) => {
  router.push(`/knowledge/${id}`);
};

const getScoreType = (score: number) => {
  if (score >= 0.6) return "success";
  if (score >= 0.3) return "warning";
  return "info";
};
</script>

<style scoped>
.knowledge-view {
  padding: 0;
}

.search-header {
  margin-bottom: 24px;
}

.search-box {
  max-width: 800px;
  margin: 0 auto;
}

.search-tip {
  margin-top: 12px;
  text-align: center;
  font-size: 13px;
  color: #909399;
}

.list-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 200px;
}

.knowledge-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.knowledge-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-color: #c0c4cc;
}

.card-main {
  flex: 1;
  min-width: 0;
}

.title {
  margin: 0 0 8px;
  font-size: 16px;
  color: #303133;
}

.snippet {
  margin: 0;
  font-size: 13px;
  color: #606266;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.score-badge {
  margin-left: 16px;
  flex-shrink: 0;
}
</style>

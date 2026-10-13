<template>
    <div class="filter-bar">
  <el-form :inline="true"  :model="localFilters" class="demo-form-inline">
    <el-form-item label="状态">
      <el-select v-model="localFilters.status" placeholder="选择状态" clearable>
        <el-option
          v-for="(item, key) in STATUS_MAP"
          :key="key"
          :label="item.label"
          :value="key"
        />
      </el-select>
    </el-form-item>
    <el-form-item label="优先级">
      <el-select
        v-model="localFilters.priority"
        placeholder="选择优先级"
        clearable
      >
        <el-option
          v-for="(item, key) in PRIORITY_MAP"
          :key="key"
          :label="item.label"
          :value="key"
        />
      </el-select>
    </el-form-item>
    <el-form-item label="关键词">
      <el-input
        v-model="localFilters.keyword"
        placeholder="关键词"
        clearable
        @keyup.enter="emitChange"
        @clear="emitChange"
      />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="emitChange">查询</el-button>
      <el-button @click="onReset">重置</el-button>
    </el-form-item>
  </el-form>

  <el-button type="primary" @click="$router.push('/tickets/create')">
      <el-icon><Plus /></el-icon>
      新建工单
    </el-button>
    </div>
</template>

<script lang="ts" setup>
import { reactive,watch } from "vue";
import { STATUS_MAP, PRIORITY_MAP } from "@/utils/constants";

export interface Filters {
  status: string;
  priority: string;
  keyword: string;
}

const props = defineProps<{
  modelValue: Filters
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: Filters): void
  (e: 'change'): void
}>()

const localFilters = reactive<Filters>({ ...props.modelValue });

watch(
    ()=>props.modelValue,
    (val)=>{
        Object.assign(localFilters,val)
    }
)
const emitChange = () => {
  emit('update:modelValue',{...localFilters})
  emit('change')
};
const onReset = () => {
  localFilters.status = "";
  localFilters.priority = "";
  localFilters.keyword = "";
  emitChange()
};
</script>

<style scoped>
.demo-form-inline .el-input {
  --el-input-width: 220px;
}

.demo-form-inline .el-select {
  --el-select-width: 220px;
}
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}
</style>
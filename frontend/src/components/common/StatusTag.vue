<template>
  <div>
    <el-tag :type="config.type as any">
        {{ config.label }}
    </el-tag>
   
  </div>
</template>

<script lang="ts" setup>
import {computed,defineProps} from 'vue'
import { STATUS_MAP, PRIORITY_MAP } from '@/utils/constants'

const props = defineProps< {
    type?: 'status' | 'priority'
    value: string
}>()

const config = computed(()=>{
    const map = props.type === 'status'? STATUS_MAP : PRIORITY_MAP
    return map[props.value] ||  { label: props.value, type: 'info' }
})
</script>   
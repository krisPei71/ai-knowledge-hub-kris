<template>
  <div class="ticket-list-view">
    <el-card shadow="never">
      <TicketFilterBar v-model="filters" @change="handleSearch" />

      <TicketTable v-loading="loading" :tickets="tickets" />

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="loadTickets"
          @size-change="handleSizeChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import {ref,reactive,onMounted} from 'vue'
import TicketFilterBar,{type Filters } from '@/components/ticket/TicketFilterBar.vue';
import TicketTable from '@/components/ticket/TicketTable.vue';
import { getTicketList,type Ticket } from '@/api/ticket';
const loading = ref(false)
const filters = reactive<Filters>({})
const tickets = ref<Ticket[]>([])
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const handleSearch=async()=>{
    loading.value=true
    try {
    const res = await getTicketList({...filters,page:page.value,page_size:pageSize.value})
    tickets.value=res.items
    total.value=res.total
    } catch (error) {
        
    }finally{
        loading.value=false
    }
}

const loadTickets = (val:number)=>{
    page.value=val
    handleSearch()
}

const handleSizeChange = (val:number)=>{
    page.value=1
    pageSize.value = val
    handleSearch()
}

onMounted(()=>{
    handleSearch()
})

</script>

<style scoped>
.ticket-list-view {
  padding: 0;
}

.pagination-wrapper {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>
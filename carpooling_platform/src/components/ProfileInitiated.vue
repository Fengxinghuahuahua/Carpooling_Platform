<template>
  <div>
    <h2 class="section-title">我发起的拼车</h2>
    <el-table :data="initiatedCarpools" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="origin" label="起点" />
      <el-table-column prop="terminal" label="终点" />
      <el-table-column prop="time" label="出发时间" width="180" />
      <el-table-column prop="seats" label="座位数" width="100" />
      <el-table-column prop="status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row?.status)">{{ row?.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="router.push(`/carpool/${row?.id}`)">查看</el-button>
          <el-button size="small" type="danger" @click="cancelCarpool(row?.id)" v-if="row?.status === '进行中'">取消</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import {ElMessage, ElMessageBox} from "element-plus";
import {onMounted, reactive} from "vue";
import {useRouter} from "vue-router";
import axios from "axios";

const router = useRouter()

// 我发起的拼车列表
const initiatedCarpools = reactive([]);

// 获取状态对应的标签类型
const getStatusType = (status) => {
  switch(status) {
    case '进行中': return 'success'
    case '已完成': return 'primary'
    case '已取消': return 'danger'
    default: return 'info'
  }
}

// 取消拼车
const cancelCarpool = (id) => {
  ElMessageBox.confirm('确定要取消这个拼车吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    const index = initiatedCarpools.findIndex(item => item.id === id)
    if (index !== -1) {
      initiatedCarpools[index].status = '已取消'
      ElMessage.success('拼车已取消')
    }
  }).catch(() => {
    ElMessage.info('已取消操作')
  })
}

onMounted(async () => {
  const newInitiatedCarpools = await axios({
    method: 'get',
    url: '/api/user/initiated_carpools',
  })
  Object.assign(initiatedCarpools, newInitiatedCarpools.data.data)
})
</script>

<style scoped>

</style>
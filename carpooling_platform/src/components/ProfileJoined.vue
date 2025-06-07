<template>
  <div>
    <h2 class="section-title">我加入的拼车</h2>
    <el-table :data="joinedCarpools" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="origin" label="起点" />
      <el-table-column prop="terminal" label="终点" />
      <el-table-column prop="time" label="出发时间" width="180" />
      <el-table-column prop="driver" label="车主" width="120" />
      <el-table-column prop="status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row?.status)">{{ row?.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="router.push(`/carpool/${row?.id}`)">查看</el-button>
          <el-button size="small" type="danger" @click="quitCarpool(row?.id)" v-if="row?.status === '进行中'">退出</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import {ElMessage, ElMessageBox} from "element-plus";
import {useRouter} from "vue-router";
import {onMounted, reactive} from "vue";
import axios from "axios";

const router = useRouter()

// 我加入的拼车列表
const joinedCarpools = reactive([]);

// 获取状态对应的标签类型
const getStatusType = (status) => {
  switch(status) {
    case '进行中': return 'success'
    case '已完成': return 'primary'
    case '已取消': return 'danger'
    default: return 'info'
  }
}

// 退出拼车
const quitCarpool = (id) => {
  ElMessageBox.confirm('确定要退出这个拼车吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    const index = joinedCarpools.findIndex(item => item.id === id)
    if (index !== -1) {
      joinedCarpools.splice(index, 1)
      ElMessage.success('已退出拼车')
    }
  }).catch(() => {
    ElMessage.info('已取消操作')
  })
}

onMounted(async () => {
  const newJoinedCarpools = await axios({
    method: 'get',
    url: '/api/user/joined_carpools'
  })
  Object.assign(joinedCarpools, newJoinedCarpools.data.data)
})
</script>

<style scoped>

</style>
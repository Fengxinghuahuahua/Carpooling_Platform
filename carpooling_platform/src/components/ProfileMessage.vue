<template>
  <div>
    <h2 class="section-title">消息中心</h2>
    <el-tabs type="border-card">
      <el-tab-pane label="未读消息">
        <el-table :data="unreadMessagesList" style="width: 100%">
          <el-table-column prop="title" label="标题" width="300"/>
          <el-table-column prop="time" label="时间" />
          <el-table-column label="操作" width="200">
            <template #default="{row}">
              <el-button size="small" @click="readMessage(row?.id)">查看</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-dialog
          title="消息详情"
          v-model="dialogVisible"
          width="500px"
          header-class="message-dialog"
        >
          <template #header="{ titleId, titleClass }">
            <div class="my-header">
              <h4 :id="titleId" :class="titleClass">消息详情</h4>
            </div>
          </template>
          <div class="message-content">
            <p><strong>标题：</strong>{{ currentMessage.title }}</p>
            <p><strong>时间：</strong>{{ currentMessage.time }}</p>
            <p><strong>内容：</strong>{{ currentMessage.content || '暂无内容' }}</p>
          </div>
          <template #footer>
            <el-button @click="dialogVisible = false">关闭</el-button>
          </template>
        </el-dialog>
      </el-tab-pane>
      <el-tab-pane label="已读消息">
        <el-table :data="readMessagesList" style="width: 100%" :column-width="180">
          <el-table-column prop="title" label="标题" width="300"/>
          <el-table-column prop="time" label="时间" />
          <el-table-column label="操作" width="200">
            <template #default="{row}">
              <el-button size="small" @click="viewMessage(row?.id)">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-dialog
          title="消息详情"
          v-model="dialogVisible"
          width="500px"
          header-class="message-dialog"
        >
          <template #header="{ titleId, titleClass }">
            <div class="my-header">
              <h4 :id="titleId" :class="titleClass">消息详情</h4>
            </div>
          </template>
          <div class="message-content">
            <p><strong>标题：</strong>{{ currentMessage.title }}</p>
            <p><strong>时间：</strong>{{ currentMessage.time }}</p>
            <p><strong>内容：</strong>{{ currentMessage.content || '暂无内容' }}</p>
          </div>
          <template #footer>
            <el-button @click="dialogVisible = false;">关闭</el-button>
          </template>
        </el-dialog>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import {ElMessage} from "element-plus";
import {onMounted, reactive, ref, defineModel} from "vue";
import service from "@/api/axios.js";

const dialogVisible = ref(false); // 控制弹窗显示
const currentMessage = ref({}); // 当前选中的消息内容

const readMessagesList = reactive([]); // 已读消息列表
const unreadMessagesList = reactive([]); // 未读消息列表
const unreadMessagesCount = defineModel(); // 未读消息数量

// 阅读未读消息
const readMessage = async (id) => {
  const index = unreadMessagesList.findIndex((item) => item.id === id);
  if (index !== -1) {
    // 发送请求更新消息状态
    await service({
      method: "post",
      url: `/api/user/messages/read/${id}`,
    });
    // 显示消息弹窗
    currentMessage.value = unreadMessagesList.splice(index, 1)[0];
    dialogVisible.value = true;
    // 发送之后重新加载数据
    await refreshData();
  } else {
    ElMessage.error('未找到该消息');
  }
};

const viewMessage = (id) => {
  const message = [...unreadMessagesList, ...readMessagesList].find(
    (item) => item.id === id
  );
  if (message) {
    currentMessage.value = message; // 设置当前消息内容
    dialogVisible.value = true; // 显示弹窗
  } else {
    ElMessage.error('未找到该消息');
  }
};

async function refreshData() {
  const newReadMessagesList = await service({
    url: '/api/user/messages/read',
    method: 'get'
  })
  Object.assign(readMessagesList, newReadMessagesList.data.data)
  const newUnreadMessagesList = await service({
    url: '/api/user/messages/unread',
    method: 'get'
  })
  Object.assign(unreadMessagesList, newUnreadMessagesList.data.data)
  unreadMessagesCount.value = newUnreadMessagesList.data.data.length
}

onMounted(async () => {
  await refreshData()
})
</script>

<style scoped>
.message-content {
  text-align: left; /* 设置内容左对齐 */
  line-height: 1.8; /* 增加行高，提升可读性 */
  font-size: 14px; /* 设置字体大小 */
  color: #333; /* 设置字体颜色 */
}

.my-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 16px;
}
</style>
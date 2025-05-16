<!--suppress CssUnusedSymbol -->
<template>
  <div class="profile-container">
    <!-- 个人信息头部 -->
    <el-card class="profile-header">
      <div class="header-content">
        <el-avatar :size="80" :src="userInfo.avatar" class="avatar" />
          <div class="user-info">
            <h2>{{ userInfo.username }}</h2>
              <p>注册时间: {{ userInfo.registerTime }}</p>
              <p>信用评分: <el-rate v-model="userInfo.creditScore" disabled /></p>
          </div>
      </div>
    </el-card>

    <!-- 导航菜单 -->
    <el-card class="profile-nav">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="我发起的拼车" name="initiated">
          <template #label>
            <span><i class="el-icon-tickets"></i> 我发起的拼车</span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="我加入的拼车" name="joined">
          <template #label>
            <span><i class="el-icon-user"></i> 我加入的拼车</span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="修改个人信息" name="edit">
          <template #label>
            <span><i class="el-icon-edit"></i> 修改个人信息</span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="消息中心" name="messages">
          <template #label>
            <span><i class="el-icon-message"></i> 消息中心</span>
            <el-badge :value="unreadMessagesCount" class="badge" v-if="unreadMessagesCount > 0" />
          </template>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 内容区域 -->
    <el-card class="content-section">
      <!-- 我发起的拼车 -->
      <ProfileInitiated v-if="activeTab === 'initiated'" />
      <!-- 我加入的拼车 -->
      <ProfileJoined v-if="activeTab === 'joined'" />
      <!-- 修改个人信息 -->
      <ProfileEdit v-if="activeTab === 'edit'" v-model="userInfo" />
      <!-- 消息中心 -->
      <ProfileMessage v-if="activeTab === 'messages'" v-model="unreadMessagesCount"/>
    </el-card>

    <!-- 退出登录按钮 -->
    <div class="logout-container">
      <el-button type="danger" @click="logout" class="logout-btn">退出登录</el-button>
    </div>
  </div>
</template>

<script setup>
import {ref, reactive, onMounted} from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import ProfileInitiated from "@/components/ProfileInitiated.vue";
import ProfileJoined from "@/components/ProfileJoined.vue";
import ProfileEdit from "@/components/ProfileEdit.vue";
import ProfileMessage from "@/components/ProfileMessage.vue";
import axios from "axios";

const router = useRouter()

// 用户信息
const userInfo = reactive({})
// 未读消息数量
const unreadMessagesCount = ref(0)

// 当前激活的标签页
const activeTab = ref('initiated')

// 退出登录
const logout = () => {
  ElMessageBox.confirm('确定要退出登录吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 这里应该是调用退出登录的API
    router.push('/login')
    ElMessage.success('已退出登录')
  }).catch(() => {
    ElMessage.info('已取消操作')
  })
}

onMounted(async () => {
  // 获取用户信息
  const newUserInfo = await axios({
    url: '/api/user/profile',
    method: 'get'
  })
  Object.assign(userInfo, newUserInfo.data.data)
  // 获取未读消息数量
  const unreadMessages = await axios({
    url: '/api/user/messages/unread',
    method: 'get'
  })
  unreadMessagesCount.value = unreadMessages.data.data.length
})
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.profile-header {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  align-items: flex-start; /* 垂直方向顶部对齐 */
  justify-content: flex-start; /* 水平方向左对齐 */
}

.user-info {
  margin-left: 20px;
  text-align: left; /* 确保文字内容左对齐 */
}

.user-info h2 {
  color: #409EFF;
  margin-bottom: 10px;
}

.profile-nav {
  margin-bottom: 20px;
}

.section-title {
  color: #409EFF;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.logout-container {
  text-align: center;
  margin-top: 20px;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar {
  width: 120px;
  height: 120px;
  display: block;
}

/* 消息中心 */
.el-dialog {
  z-index: 9999 !important;
}
</style>
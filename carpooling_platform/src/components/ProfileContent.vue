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
      <el-tabs v-model="activeTab" @tab-click="handleTabClick">
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
            <el-badge :value="unreadMessages" class="badge" v-if="unreadMessages > 0" />
          </template>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 内容区域 -->
    <el-card class="content-section">
      <!-- 我发起的拼车 -->
      <div v-if="activeTab === 'initiated'">
        <h2 class="section-title">我发起的拼车</h2>
        <el-table :data="initiatedCarpools" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="route" label="路线" />
          <el-table-column prop="time" label="出发时间" width="180" />
          <el-table-column prop="seats" label="座位数" width="100" />
          <el-table-column prop="status" label="状态" width="120">
            <template #default="{row}">
              <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180">
            <template #default="{row}">
              <el-button size="small" @click="viewCarpool(row.id)">查看</el-button>
              <el-button size="small" type="danger" @click="cancelCarpool(row.id)" 
                         v-if="row.status === '进行中'">取消</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 我加入的拼车 -->
      <div v-if="activeTab === 'joined'">
        <h2 class="section-title">我加入的拼车</h2>
        <el-table :data="joinedCarpools" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="route" label="路线" />
          <el-table-column prop="time" label="出发时间" width="180" />
          <el-table-column prop="driver" label="车主" width="120" />
          <el-table-column prop="status" label="状态" width="120">
            <template #default="{row}">
              <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180">
            <template #default="{row}">
              <el-button size="small" @click="viewCarpool(row.id)">查看</el-button>
              <el-button size="small" type="danger" @click="quitCarpool(row.id)" 
                         v-if="row.status === '进行中'">退出</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 修改个人信息 -->
      <div v-if="activeTab === 'edit'" class="edit-profile-container">
        <h2 class="person-title">修改个人信息</h2>
        <el-form :model="tempUserInfo" label-width="100px" class="edit-profile-form">
            <el-form-item label="用户名">
                <el-input v-model="tempUserInfo.username" />
            </el-form-item>
            <el-form-item label="头像">
                <el-upload
                class="avatar-uploader"
                action="/api/upload"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload">
                <img v-if="tempUserInfo.avatar" :src="tempUserInfo.avatar" class="avatar">
                <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                </el-upload>
            </el-form-item>
            <el-form-item label="手机号">
                <el-input v-model="tempUserInfo.phone" />
            </el-form-item>
            <el-form-item label="邮箱">
                <el-input v-model="tempUserInfo.email" />
            </el-form-item>
            <el-button type="primary" @click="updateProfile">保存修改</el-button>
            </el-form>
      </div>

      <!-- 消息中心 -->
      <div v-if="activeTab === 'messages'">
        <h2 class="section-title">消息中心</h2>
        <el-tabs type="border-card">
          <el-tab-pane label="未读消息">
            <el-table :data="unreadMessagesList" style="width: 100%">
              <el-table-column prop="title" label="标题" width="300"/>
              <el-table-column prop="time" label="时间" />
              <el-table-column label="操作" width="200">
                <template #default="{row}">
                  <el-button size="small" @click="readMessage(row.id)">查看</el-button>
                </template>
              </el-table-column>
            </el-table>

            <el-dialog
              title="消息详情"
              v-model="dialogVisible"
              width="500px"
            >
              <p><strong>标题：</strong>{{ currentMessage.title }}</p>
              <p><strong>时间：</strong>{{ currentMessage.time }}</p>
              <p><strong>内容：</strong>{{ currentMessage.content || '暂无内容' }}</p>
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
                  <el-button size="small" @click="viewMessage(row.id)">查看</el-button>
                </template>
              </el-table-column>
            </el-table>
            <el-dialog
              title="消息详情"
              v-model="dialogVisible"
              width="500px"
            >
              <p><strong>标题：</strong>{{ currentMessage.title }}</p>
              <p><strong>时间：</strong>{{ currentMessage.time }}</p>
              <p><strong>内容：</strong>{{ currentMessage.content || '暂无内容' }}</p>
              <template #footer>
                <el-button @click="dialogVisible = false">关闭</el-button>
              </template>
            </el-dialog>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>

    <!-- 退出登录按钮 -->
    <div class="logout-container">
      <el-button type="danger" @click="logout" class="logout-btn">退出登录</el-button>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox} from 'element-plus'
import { useRouter } from 'vue-router'

export default {
  name: 'ProfileContent',
  setup() {
    const router = useRouter()
    
    // 用户信息
    const userInfo = reactive({
      username: '拼车达人',
      avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
      phone: '13800138000',
      email: 'user@example.com',
      registerTime: '2023-01-15',
      creditScore: 4.7
    })

    // 临时对象，用于表单编辑
    const tempUserInfo = reactive({ ...userInfo })

    // 当前激活的标签页
    const activeTab = ref('initiated')

    // 我发起的拼车列表
    const initiatedCarpools = ref([
      { id: 1001, route: '北京西站 → 中关村', time: '2023-06-15 08:30', seats: 3, status: '进行中' },
      { id: 952, route: '朝阳公园 → 首都机场', time: '2023-06-10 14:00', seats: 2, status: '已完成' },
      { id: 876, route: '国贸 → 望京', time: '2023-06-05 18:00', seats: 4, status: '已取消' }
    ])

    // 我加入的拼车列表
    const joinedCarpools = ref([
      { id: 1005, route: '五道口 → 西直门', time: '2023-06-16 09:00', driver: '张师傅', status: '进行中' },
      { id: 987, route: '天通苑 → 国贸', time: '2023-06-08 07:30', driver: '李女士', status: '已完成' }
    ])

    const dialogVisible = ref(false); // 控制弹窗显示
    const currentMessage = ref({}); // 当前选中的消息内容

    // 消息相关
    const unreadMessages = ref(2)
    const unreadMessagesList = ref([
      { id: 1, title: '您的拼车申请已通过', time: '2023-06-14 10:30', content: '您的拼车申请已通过，请尽快联系车主确认详情。' },
      { id: 2, title: '系统通知: 新功能上线', time: '2023-06-13 15:45', content: '我们上线了新的拼车功能，快来体验吧！' },
    ]);

    const readMessagesList = ref([
      { id: 3, title: '欢迎使用拼车平台', time: '2023-06-01 09:00', content: '感谢您注册拼车平台，祝您使用愉快！' },
    ]);

    // 获取状态对应的标签类型
    const getStatusType = (status) => {
      switch(status) {
        case '进行中': return 'success'
        case '已完成': return ''
        case '已取消': return 'danger'
        default: return 'info'
      }
    }

    // 查看拼车详情
    const viewCarpool = (id) => {
      router.push(`/carpool/${id}`)
    }

    // 取消拼车
    const cancelCarpool = (id) => {
      ElMessageBox.confirm('确定要取消这个拼车吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = initiatedCarpools.value.findIndex(item => item.id === id)
        if (index !== -1) {
          initiatedCarpools.value[index].status = '已取消'
          ElMessage.success('拼车已取消')
        }
      }).catch(() => {
        ElMessage.info('已取消操作')
      })
    }

    // 退出拼车
    const quitCarpool = (id) => {
      ElMessageBox.confirm('确定要退出这个拼车吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = joinedCarpools.value.findIndex(item => item.id === id)
        if (index !== -1) {
          joinedCarpools.value.splice(index, 1)
          ElMessage.success('已退出拼车')
        }
      }).catch(() => {
        ElMessage.info('已取消操作')
      })
    }

    // 头像上传成功
    const handleAvatarSuccess = (res) => {
      userInfo.avatar = res.url
      ElMessage.success('头像上传成功')
    }

    // 头像上传前验证
    const beforeAvatarUpload = (file) => {
      const isJPG = file.type === 'image/jpeg'
      const isPNG = file.type === 'image/png'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG && !isPNG) {
        ElMessage.error('头像图片只能是 JPG/PNG 格式!')
      }
      if (!isLt2M) {
        ElMessage.error('头像图片大小不能超过 2MB!')
      }
      return (isJPG || isPNG) && isLt2M
    }

    // 更新个人信息
    const updateProfile = () => {
        // 校验手机号
        const phoneRegex = /^1[3-9]\d{9}$/; // 中国大陆手机号正则
        if (!phoneRegex.test(tempUserInfo.phone)) {
            ElMessage.error('请输入有效的手机号');
            return;
        }

        // 校验邮箱
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // 简单的邮箱正则
        if (!emailRegex.test(tempUserInfo.email)) {
            ElMessage.error('请输入有效的邮箱地址');
            return;
        }

        // 用户名必须为2-20个字符，且不能包含空格
        const nameRegex = /^[^\s]{2,20}$/;
        if (!nameRegex.test(tempUserInfo.username)) {
            ElMessage.error('用户名必须为2-20个字符，且不能包含空格');
            return;
        }

        // 如果校验通过，更新信息
        setTimeout(() => {
            // 假设保存成功后，更新视图
            Object.assign(userInfo, tempUserInfo);
            ElMessage.success('个人信息已更新');
        }, 500);
    }

    // 阅读消息
    const readMessage = (id) => {
      const index = unreadMessagesList.value.findIndex((item) => item.id === id);
      if (index !== -1) {
        const msg = unreadMessagesList.value.splice(index, 1)[0];
        readMessagesList.value.unshift(msg);
        unreadMessages.value--;
        currentMessage.value = msg; // 设置当前消息内容
        dialogVisible.value = true; // 显示弹窗
        ElMessage.success('消息已标记为已读');
        console.log('阅读消息:', msg);
        console.log('dialogVisible:', dialogVisible.value);
      } else {
        ElMessage.error('未找到该消息');
      }
    };

    const viewMessage = (id) => {
      const message = [...unreadMessagesList.value, ...readMessagesList.value].find(
        (item) => item.id === id
      );
      if (message) {
        currentMessage.value = message; // 设置当前消息内容
        dialogVisible.value = true; // 显示弹窗
        console.log('查看消息:', message);
        console.log('dialogVisible:', dialogVisible.value);
      } else {
        ElMessage.error('未找到该消息');
      }
    };

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

    return {
      userInfo,
      activeTab,
      initiatedCarpools,
      joinedCarpools,
      unreadMessages,
      unreadMessagesList,
      readMessagesList,
      getStatusType,
      viewCarpool,
      cancelCarpool,
      quitCarpool,
      handleAvatarSuccess,
      beforeAvatarUpload,
      updateProfile,
      readMessage,
      viewMessage,
      logout,
      tempUserInfo,
      dialogVisible,
      currentMessage
    }
  }
}
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

.person-title {
  color: #409EFF;
  margin-bottom: 0px;
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

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 120px;
  line-height: 120px;
  text-align: center;
}

.avatar {
  width: 120px;
  height: 120px;
  display: block;
}

/* 父容器设置为 flex 布局，居中内容 */
.edit-profile-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%; /* 让容器占满父级高度 */
  text-align: center;
}

/* 表单样式 */
.edit-profile-form {
  max-width: 500px;
  width: 100%;
  background: #fff;
  padding: 20px;
}

/* 消息中心 */
.el-dialog {
  z-index: 9999 !important;
}
</style>
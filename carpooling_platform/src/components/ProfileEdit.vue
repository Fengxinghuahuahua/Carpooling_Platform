<template>
  <div class="edit-profile-container">
    <h2 class="person-title">修改个人信息</h2>
    <el-form :model="userInfoCopy" label-width="100px" class="edit-profile-form">
      <el-form-item label="用户名">
        <el-input v-model="userInfoCopy.username" />
      </el-form-item>
      <el-form-item label="头像">
        <el-upload
          class="avatar-uploader"
          action="/api/user/upload"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :before-upload="beforeAvatarUpload"
          :http-request="customUpload"
        >
          <img v-if="userInfoCopy.avatar" :src="userInfoCopy.avatar" class="avatar" alt="头像">
          <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
        </el-upload>
      </el-form-item>
      <el-form-item label="手机号">
        <el-input v-model="userInfoCopy.phone" />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="userInfoCopy.email" />
      </el-form-item>
      <el-button type="primary" @click="updateProfile">保存修改</el-button>
    </el-form>
  </div>
</template>

<script setup>
import {ElMessage} from "element-plus";
import {defineModel, reactive} from "vue";
import service from "@/api/axios.js";
import {Plus} from "@element-plus/icons-vue";

const userInfo = defineModel()

// 用户信息副本，用于表单编辑
const userInfoCopy = reactive({
  username: userInfo.value.username,
  avatar: userInfo.value.avatar,
  phone: userInfo.value.phone,
  email: userInfo.value.email
})

// 头像上传前验证
const beforeAvatarUpload = (rawFile) => {
  const isJPG = rawFile.type === 'image/jpeg'
  const isPNG = rawFile.type === 'image/png'
  const isLt2M = rawFile.size / 1024 / 1024 < 2

  if (!isJPG && !isPNG)
    ElMessage.error('头像图片只能是 JPG/PNG 格式!')
  if (!isLt2M)
    ElMessage.error('头像图片大小不能超过 2MB!')
  return (isJPG || isPNG) && isLt2M
}

// 自定义上传函数
const customUpload = (option) => {
  const reader = new FileReader()
  reader.readAsDataURL(option.file)
  reader.onload = () => {
    service.post('/api/user/upload', {
      data: reader.result
    }).then((res) => {
      option.onSuccess(res)
    })
  }
}

// 头像上传成功
const handleAvatarSuccess = (res) => {
  userInfoCopy.avatar = res.data.data
  ElMessage.success('头像上传成功')
}

// 更新个人信息
const updateProfile = () => {
  // 校验手机号
  const phoneRegex = /^1[3-9]\d{9}$/; // 中国大陆手机号正则
  if (!phoneRegex.test(userInfoCopy.phone)) {
    ElMessage.error('请输入有效的手机号');
    return;
  }
  // 校验邮箱
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // 简单的邮箱正则
  if (!emailRegex.test(userInfoCopy.email)) {
    ElMessage.error('请输入有效的邮箱地址');
    return;
  }
  // 用户名必须为2-20个字符，且不能包含空格
  const nameRegex = /^\S{2,20}$/;
  if (!nameRegex.test(userInfoCopy.username)) {
    ElMessage.error('用户名必须为2-20个字符，且不能包含空格');
    return;
  }
  // 如果校验通过，更新信息
  service({
    method: 'post',
    url: '/api/user/update',
    data: userInfoCopy
  }).then(() => {
    // 刷新原始数据
    userInfo.value.username = userInfoCopy.username
    userInfo.value.avatar = userInfoCopy.avatar
    userInfo.value.phone = userInfoCopy.phone
    userInfo.value.email = userInfoCopy.email
    ElMessage.success('个人信息已更新');
  }).catch(() => {
    ElMessage.error('更新失败，请稍后再试');
  })
}
</script>

<style scoped>
.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>

<style>
.person-title {
  color: #409EFF;
  margin-bottom: 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
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
</style>
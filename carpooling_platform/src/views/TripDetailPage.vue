<template>
  <div class="page-container trip-detail-page">
    <div v-if="isLoading" class="loading-spinner"></div>
    <div v-if="error && !isLoading" class="error-message">{{ error }}</div> <!-- 只有在非加载状态下显示错误 -->
    <div v-if="trip && !isLoading && !error" class="trip-content">
      <div class="trip-header">
        <h2>{{ trip.departure }} ➔ {{ trip.destination }}</h2>
        <span :class="['status-badge', trip.status === '可拼' ? 'status-available' : 'status-full']">
          {{ trip.status }} (还剩 {{ trip.current_people }}座 / 共{{trip.max_people}}座)
        </span>
      </div>

      <div class="info-section">
        <p><strong>出发时间:</strong> {{ formatDateTime(trip.departureTime) }}</p>
        <p><strong>发布时间:</strong> {{ formatDateTime(trip.publishTime) }}</p>
        <p><strong>描述信息:</strong> {{ trip.description }}</p>
        <p><strong>{{ trip.hasCar ? '车主提供车辆' : '乘客寻求车辆' }}</strong></p>
      </div>

      <div class="driver-section">
        <h4>发起人信息</h4>
        <div class="driver-info">
          <img :src="trip.driver && trip.driver.avatar ? trip.driver.avatar : defaultAvatar" alt="driver avatar" class="avatar-large">
          <div class="driver-details">
            <p><strong>{{ trip.driver ? trip.driver.name : '未知' }}</strong></p>
            <p v-if="trip.driver">身份: {{ trip.driver.isDriver ? (trip.hasCar ? '车主' : '发起人-有车') : '发起人-无车' }}</p>
          </div>
        </div>
      </div>

      <div class="passengers-section">
        <h4>已加入的拼车伙伴 ({{ trip.passengers ? trip.passengers.length : 0 }}人)</h4>
        <ul v-if="trip.passengers && trip.passengers.length > 0" class="passenger-list">
          <li v-for="passenger in trip.passengers" :key="passenger.id" class="passenger-item">
            <img :src="passenger.avatar || defaultAvatar" alt="passenger avatar" class="avatar-small">
            <span>{{ passenger.name }}</span>
          </li>
        </ul>
        <p v-else>还没有人加入，快来成为第一个吧！</p>
      </div>

      <div class="actions-section">
        <button v-if="canJoin" @click="joinTrip" class="btn btn-primary" :disabled="isProcessing || !currentUser">
          {{ isProcessing ? '处理中...' : '加入拼车' }} <!-- 简化按钮文字 -->
        </button>
        <button v-if="isJoined" @click="leaveTrip" class="btn btn-warning" :disabled="isProcessing || !currentUser">
          {{ isProcessing ? '处理中...' : '退出拼车' }}
        </button>
        <button v-if="isInitiator" @click="deleteTrip" class="btn btn-danger" :disabled="isProcessing || !currentUser">
          {{ isProcessing ? '处理中...' : '删除本次拼车' }}
        </button>
        <p v-if="actionMessage" :class="actionStatus === 'success' ? 'success-message' : 'error-message'">
          {{ actionMessage }}
        </p>
        <p v-if="!currentUser && (trip && trip.status === '可拼')" class="info-message">
          请<router-link to="/login">登录</router-link>后进行操作。
        </p>
      </div>
    </div>
    <div v-if="!trip && !isLoading && !error" class="not-found">
      <p>未找到该行程信息。</p>
      <router-link to="/home" class="btn btn-secondary">返回首页</router-link>
    </div>
  </div>
</template>

<script>
import service from "@/api/axios.js";
import defaultAvatar from '@/assets/images/avatar_default.png'; // 确保这个路径正确

export default {
  name: 'TripDetailPage',
  props: ['id'],
  data() {
    return {
      trip: null,
      isLoading: true, // 初始设为 true，因为要先加载数据
      isProcessing: false,
      error: null,
      actionMessage: '',
      actionStatus: '',
      currentUser: null, // 仍然需要 currentUser 来判断按钮的显示和操作权限
      defaultAvatar: defaultAvatar
    };
  },
  computed: {
    isInitiator() {
      // 确保 trip 和 trip.driver 存在
      return this.trip && this.trip.driver && this.currentUser && this.trip.driver.id === this.currentUser.id;
    },
    isJoined() {
      // 确保 trip 和 trip.passengers 存在
      return this.trip && this.trip.passengers && this.currentUser && this.trip.passengers.some(p => p.id === this.currentUser.id);
    },
    canJoin() {
      // 确保 trip 和 trip.passengers 存在
      return this.trip && this.trip.passengers && this.currentUser &&
             !this.isInitiator && !this.isJoined &&
             this.trip.passengers.length < this.trip.seatsTotal &&
             this.trip.status === '可拼';
    },
    // 从 trip 对象中直接获取 seatsAvailable，如果 mock API 已经计算好了
    // 如果 mock API 没有计算，我们可以在这里计算或在 fetchTripDetails 后计算
    // seatsAvailable() {
    //   if (this.trip && this.trip.seatsTotal && this.trip.passengers) {
    //     return this.trip.seatsTotal - this.trip.passengers.length;
    //   }
    //   return 0;
    // }
  },
  created() {
    this.loadCurrentUser(); // 仍然加载当前用户，用于UI判断和操作权限
    if (this.id) { // 确保 id 存在才去获取详情
        this.fetchTripDetails();
    } else {
        this.error = "无效的行程ID。";
        this.isLoading = false;
    }
  },
  methods: {
    loadCurrentUser() {
      const storedUser = localStorage.getItem('currentUser');
      if (storedUser) {
        try {
          this.currentUser = JSON.parse(storedUser);
        } catch (e) {
          console.error("Error parsing currentUser from localStorage:", e);
          this.currentUser = null;
          // 不再在这里清除 token 或重定向，交给路由守卫处理
        }
      } else {
        this.currentUser = null; // 用户未登录
      }
    },
    async fetchTripDetails() {
      this.isLoading = true;
      this.error = null;
      this.trip = null; // 重置 trip
      try {
        const response = await service.get(`/api/trips/${this.id}`);
        if (response.data.code === 200 && response.data.data) {
          this.trip = response.data.data;
          console.log(this.trip)
          // 确保 mock API 返回的 trip 对象中包含 seatsAvailable，或者在这里计算
          if (typeof this.trip.seatsAvailable === 'undefined' && this.trip.passengers) {
              this.trip.seatsAvailable = this.trip.seatsTotal - this.trip.passengers.length;
          }
        } else {
          this.error = response.data.message || '获取行程详情失败';
        }
      } catch (err) {
        console.error('Error fetching trip details:', err);
        this.error = '网络错误，无法获取行程详情。';
      } finally {
        this.isLoading = false;
      }
    },
    formatDateTime(dateTimeStr) {
      if (!dateTimeStr) return '未知时间';
      try {
        const date = new Date(dateTimeStr.replace(/-/g, '/')); // 兼容 Safari
        if (isNaN(date.getTime())) { // 检查日期是否有效
            return '无效日期格式';
        }
        return date.toLocaleString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' });
      } catch (e) {
        console.error("Error formatting date:", dateTimeStr, e);
        return "日期解析错误";
      }
    },
    // 加入、退出、删除行程的方法保持不变，但它们内部会先检查 this.currentUser
    async joinTrip() {
      if (!this.currentUser) {
        this.showActionMessage("请先登录后再操作。", "error");
        return;
      }
      this.isProcessing = true;
      this.clearActionMessage();
      try {
        const response = await service.post(`/api/trips/${this.id}/join`);
        if (response.data.code === 200) {
          this.trip = response.data.data;
           if (typeof this.trip.seatsAvailable === 'undefined' && this.trip.passengers) { // 更新 seatsAvailable
              this.trip.seatsAvailable = this.trip.seatsTotal - this.trip.passengers.length;
          }
          this.showActionMessage('成功加入拼车！', 'success');
        } else {
          this.showActionMessage(response.data.message || '加入失败', 'error');
        }
      } catch (err) {
        console.error("Join trip error:", err);
        this.showActionMessage(err.response?.data?.message || '操作失败，请稍后再试。', 'error');
      } finally {
        this.isProcessing = false;
      }
    },
    async leaveTrip() {
      if (!this.currentUser) {
        this.showActionMessage("请先登录后再操作。", "error");
        return;
      }
      this.isProcessing = true;
      this.clearActionMessage();
      try {
        const response = await service.post(`/api/trips/${this.id}/leave`);
        if (response.data.code === 200) {
          this.trip = response.data.data;
          if (typeof this.trip.seatsAvailable === 'undefined' && this.trip.passengers) { // 更新 seatsAvailable
              this.trip.seatsAvailable = this.trip.seatsTotal - this.trip.passengers.length;
          }
          this.showActionMessage('已成功退出拼车。', 'success');
        } else {
          this.showActionMessage(response.data.message || '退出失败', 'error');
        }
      } catch (err) {
        console.error("Leave trip error:", err);
        this.showActionMessage(err.response?.data?.message || '操作失败，请稍后再试。', 'error');
      } finally {
        this.isProcessing = false;
      }
    },
    async deleteTrip() {
      if (!this.currentUser) {
        this.showActionMessage("请先登录后再操作。", "error");
        return;
      }
      // 确保是发起人才能删除
      if (!this.isInitiator) {
        this.showActionMessage("您无权删除此行程。", "error");
        return;
      }
      if (!confirm('确定要删除这个拼车行程吗？此操作不可撤销。')) {
        return;
      }
      this.isProcessing = true;
      this.clearActionMessage();
      try {
        const response = await service.delete(`/api/trips/${this.id}`);
        if (response.data.code === 200) {
          this.showActionMessage('行程删除成功！正在跳转回首页...', 'success');
          setTimeout(() => this.$router.push('/home'), 2000);
        } else {
          this.showActionMessage(response.data.message || '删除失败', 'error');
        }
      } catch (err) {
        console.error("Delete trip error:", err);
        this.showActionMessage(err.response?.data?.message || '操作失败，请稍后再试。', 'error');
      } finally {
        this.isProcessing = false;
      }
    },
    showActionMessage(message, status) {
      this.actionMessage = message;
      this.actionStatus = status;
      setTimeout(() => {
        this.clearActionMessage();
      }, 3000);
    },
    clearActionMessage() {
      this.actionMessage = '';
      this.actionStatus = '';
    }
  }
};
</script>

<style scoped>
.trip-detail-page {}
.trip-content {}
.trip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}
.trip-header h2 {
  margin: 0;
  color: #007bff;
}
.status-badge {
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.9em;
  color: white;
}
.status-available { background-color: #28a745; }
.status-full { background-color: #dc3545; }

.info-section, .driver-section, .passengers-section, .actions-section {
  margin-bottom: 25px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 6px;
}
.info-section p, .driver-details p {
  margin: 8px 0;
  line-height: 1.6;
}
.driver-section h4, .passengers-section h4 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
  border-bottom: 1px solid #ddd;
  padding-bottom: 8px;
}
.driver-info {
  display: flex;
  align-items: center;
}
.avatar-large {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin-right: 15px;
  object-fit: cover;
  border: 2px solid #eee;
}
.passenger-list {
  list-style: none;
  padding: 0;
}
.passenger-item {
  display: flex;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px dotted #eee;
}
.passenger-item:last-child {
  border-bottom: none;
}
.avatar-small {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}
.actions-section button {
  margin-right: 10px;
  margin-bottom: 10px;
}
.btn-warning {
  background-color: #ffc107;
  color: #212529;
}
.btn-warning:hover {
  background-color: #e0a800;
}
.not-found {
  text-align: center;
  padding: 30px;
}
.not-found p {
  margin-bottom: 20px;
  font-size: 1.2em;
}
.error-message {
  color: red;
  margin-bottom: 15px;
  text-align: center;
}
.info-message {
  color: #666;
  font-size: 0.9em;
  margin-top: 10px;
}
.info-message a {
  color: #007bff;
  text-decoration: underline;
}
.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 20px auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
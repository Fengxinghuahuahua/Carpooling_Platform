<template>
  <div class="page-container publish-trip-page">
    <h2 class="page-title">发布新的拼车</h2>
    <form @submit.prevent="submitTrip">
      <div class="form-group">
        <label for="origin">出发地:</label>
        <input type="text" id="origin" v-model="trip.origin" placeholder="例如：辣椒坊肉" required>
      </div>
      <div class="form-group">
        <label for="destination">目的地:</label>
        <input type="text" id="destination" v-model="trip.destination" placeholder="例如：华理轻院" required>
      </div>
      <div class="form-group">
        <label for="departureTime">出发时间:</label>
        <input type="datetime-local" id="departureTime" v-model="trip.departureTime" required>
      </div>
      <div class="form-group">
        <label for="description">描述信息:</label>
        <textarea id="description" v-model="trip.description" placeholder="例如：吃完饭回学校，有一起的没？"></textarea>
      </div>
      <div class="form-group">
        <label for="seatsTotal">可载人数 (除司机外):</label>
        <input type="number" id="seatsTotal" v-model.number="trip.seatsTotal" min="1" max="10" required>
      </div>
      <div class="form-group">
        <label>我是否提供车辆:</label>
        <div class="radio-group">
          <label><input type="radio" v-model="trip.hasCar" :value="true"> 是，我开车</label>
          <label><input type="radio" v-model="trip.hasCar" :value="false"> 否，我找车</label>
        </div>
      </div>

      <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
        {{ isSubmitting ? '发布中...' : '确认发布' }}
      </button>

      <!-- 本地消息提示可以保留，用于显示表单验证错误 -->
      <p v-if="message && isError" class="error-message">{{ message }}</p>
    </form>
  </div>
</template>

<script>
import service from "@/api/axios.js";
// --- 关键修改 1: 导入 ElMessage ---
import { ElMessage } from 'element-plus';

export default {
  name: 'PublishTripPage',
  data() {
    return {
      trip: {
        origin: '',
        destination: '',
        departureTime: this.getDefaultDepartureTime(),
        description: '',
        seatsTotal: 1, // 默认为1
        hasCar: true
      },
      isSubmitting: false,
      message: '',
      isError: false
    };
  },
  methods: {
    getDefaultDepartureTime() {
      const now = new Date();
      // 增加一小时作为默认出发时间
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset() + 60);
      // 返回 HTML datetime-local input 需要的格式
      return now.toISOString().slice(0, 16);
    },
    async submitTrip() {
      this.isSubmitting = true;
      this.message = '';
      this.isError = false;

      // 前端验证
      if (!this.trip.origin || !this.trip.destination || !this.trip.departureTime || this.trip.seatsTotal <= 0) {
        this.message = '请填写所有必填项。';
        this.isError = true;
        this.isSubmitting = false;
        return;
      }

      try {
        const payload = {
          origin: this.trip.origin,
          destination: this.trip.destination,
          departureTime: this.trip.departureTime,
          seatsTotal: this.trip.seatsTotal,
          description: this.trip.description,
          hasCar: this.trip.hasCar
        };
        
        const response = await service.post('/api/trips/', payload);

        if (response.data.code === 201) {
          // --- 关键修改 2: 使用 ElMessage 显示成功消息 ---
          ElMessage.success('行程发布成功！即将跳转到详情页...');
          
          setTimeout(() => {
            // 使用 name 跳转，并传递新行程的 ID
            this.$router.push({ name: 'TripDetail', params: { id: response.data.data.id } });
          }, 1500);
        } else {
          // 对于接口返回的业务失败，也使用 ElMessage
          ElMessage.error(response.data.message || '发布失败，请稍后再试。');
        }
      } catch (error) {
        console.error('Error publishing trip:', error);
        // 网络错误或被拦截器处理的错误，也使用 ElMessage
        // 拦截器中可能已经弹过消息，这里可以作为备用
        if (!error.response || error.response.status !== 401) {
            ElMessage.error(error.response?.data?.message || '发布过程中发生错误，请检查网络。');
        }
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
.publish-trip-page {
  max-width: 600px;
}
</style>
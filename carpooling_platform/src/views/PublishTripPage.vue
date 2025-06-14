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

      <p v-if="message" :class="isError ? 'error-message' : 'success-message'">{{ message }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PublishTripPage',
  data() {
    return {
      trip: {
        origin: '',
        destination: '',
        departureTime: this.getDefaultDepartureTime(),
        description: '',
        seatsTotal: 3,
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
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset() + 60);
      return now.toISOString().slice(0, 16);
    },
    async submitTrip() {
      this.isSubmitting = true;
      this.message = '';
      this.isError = false;

      if (!this.trip.origin || !this.trip.destination || !this.trip.departureTime || this.trip.seatsTotal <= 0) {
        this.message = '请填写所有必填项。';
        this.isError = true;
        this.isSubmitting = false;
        return;
      }

      const formattedDepartureTime = this.trip.departureTime.replace('T', ' ').replace(/-/g, '/');


      try {
        const payload = {
          ...this.trip,
          departureTime: formattedDepartureTime
        };
        const response = await axios.post('/api/trips', payload);
        if (response.data.code === 200) {
          this.message = '行程发布成功！';
          // 重置表单或跳转
          setTimeout(() => {
            this.$router.push({ name: 'TripDetailPage', params: { id: response.data.data.id } });
          }, 1500);
        } else {
          this.message = response.data.message || '发布失败，请稍后再试。';
          this.isError = true;
        }
      } catch (error) {
        console.error('Error publishing trip:', error);
        this.message = '发布过程中发生错误，请检查网络或联系管理员。';
        this.isError = true;
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
/* PublishTripPage specific styles, if any, can go here */
/* General form styles are in global.css */
.publish-trip-page {
  max-width: 600px; /* narrower form */
}
</style>
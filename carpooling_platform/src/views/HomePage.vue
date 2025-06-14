<template>
  <div class="page-container home-page">
    <div v-if="announcement" class="announcement-bar">
      📢 {{ announcement }}
    </div>

    <div v-if="isLoading" class="loading-spinner"></div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="!isLoading && !error && trips.length === 0" class="empty-state">
      <p>目前还没有拼车信息，快去发布一个吧！</p>
      <button @click="goToPublish" class="btn btn-primary">发布行程</button>
    </div>

    <div v-if="trips.length > 0" class="trip-list">
      <trip-card v-for="trip in trips" :key="trip.id" :trip="trip" />
    </div>
  </div>
</template>

<script>
import TripCard from '@/components/TripCard.vue';
import service from "@/api/axios.js";

export default {
  name: 'HomePage',
  components: {
    TripCard
  },
  data() {
    return {
      trips: [],
      isLoading: false,
      error: null,
      announcement: '上海市关于共享单车有序停放的通告'
    };
  },
  created() {
    this.fetchTrips();
  },
  methods: {
    async fetchTrips() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await service.get('/api/trips');
        if (response.data.code === 200) {
          this.trips = response.data.data;
        } else {
          this.error = response.data.message || '获取行程失败';
        }
      } catch (err) {
        console.error('Error fetching trips:', err);
        this.error = '网络错误，无法获取行程信息。';
      } finally {
        this.isLoading = false;
      }
    },
    goToPublish() {
      this.$router.push('/publish');
    }
  }
};
</script>

<style scoped>
.home-page {
  padding-top: 10px; /* 调整与header的间距 */
}
.announcement-bar {
  background-color: #fffbe6; /* 淡黄色背景 */
  border: 1px solid #ffe58f;
  color: #fa8c16;
  padding: 10px 15px;
  border-radius: 4px;
  margin-bottom: 20px;
  text-align: center;
}
.trip-list {
  margin-top: 20px;
}
.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #777;
}
.empty-state p {
  margin-bottom: 20px;
  font-size: 1.1em;
}
</style>
<template>
  <div class="page-container search-trip-page">
    <h2 class="page-title">行程搜索</h2>
    <form @submit.prevent="performSearch" class="search-form">
      <div class="form-group">
        <label for="search-origin">出发地:</label>
        <input type="text" id="search-origin" v-model="searchParams.origin" placeholder="例如：唐山北站">
      </div>
      <div class="form-group">
        <label for="search-destination">目的地:</label>
        <input type="text" id="search-destination" v-model="searchParams.destination" placeholder="输入地点关键字">
      </div>
      <div class="form-row">
        <div class="form-group half-width">
          <label for="search-earliestTime">最早时间:</label>
          <input type="date" id="search-earliestTime" v-model="searchParams.earliestTime">
        </div>
        <div class="form-group half-width">
          <label for="search-latestTime">最晚时间:</label>
          <input type="date" id="search-latestTime" v-model="searchParams.latestTime">
        </div>
      </div>
      <div class="form-group">
        <label>是否有车:</label>
        <div class="radio-group">
          <label><input type="radio" v-model="searchParams.hasCar" value="any"> 不限</label>
          <label><input type="radio" v-model="searchParams.hasCar" value="true"> 有车 (我是乘客)</label>
          <label><input type="radio" v-model="searchParams.hasCar" value="false"> 无车 (我是车主)</label>
        </div>
      </div>
      <button type="submit" class="btn btn-primary" :disabled="isSearching">
        {{ isSearching ? '搜索中...' : '根据条件筛选' }}
      </button>
    </form>

    <div class="search-results">
      <h3 v-if="searchedOnce && !isSearching">搜索结果 ({{ searchResults.length }})</h3>
      <div v-if="isSearching" class="loading-spinner"></div>
      <div v-if="searchError" class="error-message">{{ searchError }}</div>

      <div v-if="!isSearching && searchedOnce && searchResults.length === 0 && !searchError" class="empty-state">
        <p>没有找到符合条件的拼车信息。</p>
      </div>

      <trip-card v-for="trip in searchResults" :key="trip.id" :trip="trip" />
    </div>
  </div>
</template>

<script>
import service from "@/api/axios.js";
import TripCard from '@/components/TripCard.vue';

export default {
  name: 'SearchTripPage',
  components: {
    TripCard
  },
  data() {
    return {
      searchParams: {
        origin: '',
        destination: '',
        earliestTime: '',
        latestTime: '',
        hasCar: 'any'
      },
      searchResults: [],
      isSearching: false,
      searchError: null,
      searchedOnce: false
    };
  },
  methods: {
    async performSearch() {
      this.isSearching = true;
      this.searchError = null;
      this.searchedOnce = true;
      this.searchResults = [];

      const query = {};
      if (this.searchParams.origin) query.origin = this.searchParams.origin;
      if (this.searchParams.destination) query.destination = this.searchParams.destination;
      if (this.searchParams.earliestTime) query.earliestTime = this.searchParams.earliestTime.replace(/-/g, '/');
      if (this.searchParams.latestTime) query.latestTime = this.searchParams.latestTime.replace(/-/g, '/');
      if (this.searchParams.hasCar !== 'any') query.hasCar = this.searchParams.hasCar;

      try {
        const response = await service.get('/api/trips/search', { params: query });
        if (response.data.code === 200) {

          this.searchResults = response.data.data;
        } else {
          this.searchError = response.data.message || '搜索失败';
        }
      } catch (error) {
        console.error('Error searching trips:', error);
        this.searchError = '搜索过程中发生错误，请稍后再试。';
      } finally {
        this.isSearching = false;
      }
    }
  }
};
</script>

<style scoped>
.search-form {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}
.form-row {
  display: flex;
  gap: 20px; /* space between half-width inputs */
}
.half-width {
  flex: 1;
}
.search-results h3 {
  margin-top: 20px;
  margin-bottom: 15px;
  color: #333;
}
.empty-state {
  text-align: center;
  padding: 30px 20px;
  color: #777;
}
</style>
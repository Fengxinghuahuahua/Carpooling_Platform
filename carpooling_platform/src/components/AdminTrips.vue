<template>
  <div>
    <h3>行程管理</h3>

    <div v-if="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <table v-if="!loading && trips.length" class="trip-table">
      <thead>
        <tr>
          <th>发布用户</th>
          <th>出发地</th>
          <th>目的地</th>
          <th>出发时间</th>
          <th>发布时间</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="trip in trips" :key="trip.id">
          <td>
            <img :src="trip.driver.avatar" alt="头像" class="avatar" />
            {{ trip.driver.name }}
          </td>
          <td>{{ trip.origin }}</td>
          <td>{{ trip.destination }}</td>
          <td>{{ trip.departureTime }}</td>
          <td>{{ trip.publishTime }}</td>
          <td>{{ trip.status }}</td>
          <td>
            <button @click="deleteTrip(trip.id)" class="delete-btn">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="!loading && trips.length === 0">暂无行程数据。</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminTrips',
  data() {
    return {
      trips: [],
      loading: false,
      error: null,
    };
  },
  methods: {
    fetchTrips() {
      this.loading = true;
      axios.get('/api/trips')
        .then(res => {
          if (res.data.code !== 200) throw new Error(res.data.message || '获取失败');
          this.trips = res.data.data || [];
        })
        .catch(err => {
          this.error = err.response?.data?.error || err.message;
          this.trips = [];
        })
        .finally(() => {
          this.loading = false;
        });
    },
    deleteTrip(id) {
      if (!confirm('确定删除该行程吗？')) return;
      axios.delete(`/api/trips/${id}`)
        .then(res => {
          if (res.data.code !== 200) throw new Error(res.data.message || '删除失败');
          alert('删除成功');
          this.fetchTrips();
        })
        .catch(err => {
          alert('删除失败: ' + (err.response?.data?.error || err.message));
        });
    },
  },
  mounted() {
    this.fetchTrips();
  },
};
</script>

<style scoped>
.trip-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
.trip-table th,
.trip-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
.trip-table th {
  background-color: #f2f2f2;
}
.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 5px;
  vertical-align: middle;
}
.delete-btn {
  background-color: #e74c3c;
  border: none;
  color: white;
  padding: 6px 12px;
  border-radius: 3px;
  cursor: pointer;
}
.delete-btn:hover {
  background-color: #c0392b;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>

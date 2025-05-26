<template>
  <div class="trip-card" @click="goToDetail">
    <div class="card-header">
      <span class="origin-dest">{{ trip.origin }} ➔ {{ trip.destination }}</span>
      <span :class="['status-badge', trip.status === '可拼' ? 'status-available' : 'status-full']">
        {{ trip.status }}
      </span>
    </div>
    <div class="card-body">
      <p><strong>出发时间:</strong> {{ formatDateTime(trip.departureTime) }}</p>
      <p class="description"><strong>描述:</strong> {{ trip.description }}</p>
      <p>
        <strong>{{ trip.hasCar ? '提供车辆' : '寻求车辆' }}</strong> |
        <strong>可载/总座位:</strong> {{ trip.seatsAvailable }} / {{ trip.seatsTotal }}
      </p>
    </div>
    <div class="card-footer">
      <div class="driver-info">
        <img :src="trip.driver.avatar || defaultAvatar" alt="driver" class="avatar">
        <span>{{ trip.driver.name }} {{ trip.hasCar ? '(车主)' : '(发起人)' }}</span>
      </div>
      <span class="publish-time">发布于: {{ formatDateTime(trip.publishTime, true) }}</span>
    </div>
  </div>
</template>

<script>
import defaultAvatar from '@/assets/images/avatar_default.png';

export default {
  name: 'TripCard',
  props: {
    trip: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      defaultAvatar: defaultAvatar
    };
  },
  methods: {
    goToDetail() {
      this.$router.push({ name: 'TripDetailPage', params: { id: this.trip.id } });
    },
    formatDateTime(dateTimeStr, dateOnly = false) {
      if (!dateTimeStr) return '未知时间';
      const date = new Date(dateTimeStr.replace(/-/g, '/')); // 兼容性处理
      if (dateOnly) {
        return date.toLocaleDateString();
      }
      return date.toLocaleString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    }
  },
  computed: {
    seatsAvailable() {
        return this.trip.seatsTotal - this.trip.passengers.length;
    }
  }
};
</script>

<style scoped>
.trip-card {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 15px;
  padding: 15px;
  cursor: pointer;
  transition: box-shadow 0.2s ease;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.trip-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px dashed #eee;
}
.origin-dest {
  font-weight: bold;
  font-size: 1.2em;
  color: #007bff;
}
.status-badge {
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  color: white;
  font-weight: 500;
}
.status-available {
  background-color: #28a745; /* 绿色 */
}
.status-full {
  background-color: #dc3545; /* 红色 */
}
.status-inprogress {
  background-color: #ffc107; /* 黄色 */
  color: #333;
}
.card-body p {
  margin: 5px 0;
  color: #555;
  font-size: 0.95em;
}
.description {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 90%;
}
.card-footer {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85em;
  color: #777;
}
.driver-info {
  display: flex;
  align-items: center;
}
.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 8px;
  object-fit: cover;
}
</style>
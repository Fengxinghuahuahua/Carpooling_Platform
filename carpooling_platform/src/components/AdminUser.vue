<template>
  <div class="admin-layout">
    <div class="sidebar">
      <h2>管理员后台</h2>
      <ul>
        <li @click="current = 'users'" :class="{ active: current === 'users' }">管理用户</li>
        <li @click="current = 'trips'" :class="{ active: current === 'trips' }">管理行程</li>
        <li @click="current = 'managers'" :class="{ active: current === 'managers' }">管理管理员</li>
        <li @click="logout">退出登录</li>
      </ul>
    </div>
    <div class="main-content">
      <!-- 用户管理内容 -->
      <div v-if="current === 'users'">
        <h3>用户管理</h3>

        <div v-if="loading">加载中...</div>
        <div v-if="error" class="error">{{ error }}</div>

        <table v-if="!loading && users.length" class="user-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>手机号</th>
              <th>邮箱</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.phone }}</td>
              <td>{{ user.email }}</td>
              <td>
                <button @click="deleteUser(user.id)" class="delete-btn">删除</button>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="!loading && users.length === 0">
          暂无用户数据。
        </div>
      </div>

      <!-- 管理行程 -->
      <AdminTrips v-if="current === 'trips'" />

      <!-- 管理管理员 -->
      <AdminManagers v-if="current === 'managers'" />
    </div>
  </div>
</template>

<script>
import AdminTrips from './AdminTrips.vue';
import AdminManagers from './AdminManagers.vue';
import axios from 'axios';

export default {
  name: 'AdminUser',
  components: {
    AdminTrips,
    AdminManagers,
  },
  data() {
    return {
      current: 'users',
      users: [],
      loading: false,
      error: null,
    };
  },
  methods: {
    fetchUsers() {
      this.loading = true;
      this.error = null;
      axios.get('/api/users')
        .then(res => {
          // axios 返回的数据一般在 res.data
          if (res.data.code !== 200) {
            throw new Error(res.data.message || '获取用户列表失败');
          }
          this.users = res.data.data || [];
        })
        .catch(err => {
          // axios 错误时 err.response 可能包含后端返回的信息
          this.error = err.response?.data?.error || err.message || '获取用户列表失败';
          this.users = [];
        })
        .finally(() => {
          this.loading = false;
        });
    },
    deleteUser(userId) {
      if (!confirm('确定删除该用户吗？')) return;
      axios.delete(`/api/users/${userId}`)
        .then(res => {
          if (res.data.code !== 200) {
            throw new Error(res.data.message || '删除失败');
          }
          alert('删除成功');
          this.fetchUsers();
        })
        .catch(err => {
          alert('删除失败: ' + (err.response?.data?.error || err.message || '删除失败'));
        });
    },
    logout() {
      // 清除认证信息等
      this.$router.push('/login');
    },
  },
  watch: {
    current(newVal) {
      if (newVal === 'users') {
        this.fetchUsers();
      }
    },
  },
  mounted() {
    if (this.current === 'users') {
      this.fetchUsers();
    }
  },
};
</script>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  font-family: Arial, sans-serif;
}

.sidebar {
  width: 200px;
  background-color: #2c3e50;
  color: white;
  padding: 20px;
}

.sidebar h2 {
  margin-bottom: 20px;
  font-size: 20px;
  text-align: center;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  padding: 10px;
  cursor: pointer;
  border-radius: 4px;
  user-select: none;
}

.sidebar li.active,
.sidebar li:hover {
  background-color: #1abc9c;
}

.main-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.user-table th,
.user-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.user-table th {
  background-color: #f2f2f2;
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

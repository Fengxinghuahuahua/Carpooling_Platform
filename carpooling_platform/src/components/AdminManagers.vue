<template>
  <div>
    <h3>管理员管理</h3>

    <div v-if="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <!-- 添加管理员表单 -->
    <form @submit.prevent="addManager" class="add-form">
      <input v-model="newManager.username" placeholder="用户名" required />
      <input v-model="newManager.password" type="password" placeholder="密码" required />
      <input v-model="newManager.phone" placeholder="手机号" />
      <input v-model="newManager.email" placeholder="邮箱" />
      <button type="submit">添加管理员</button>
    </form>

    <table v-if="!loading && managers.length" class="manager-table">
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
        <tr v-for="manager in managers" :key="manager.id">
          <td>{{ manager.id }}</td>
          <td>{{ manager.username }}</td>
          <td>{{ manager.phone }}</td>
          <td>{{ manager.email }}</td>
          <td>
            <button @click="deleteManager(manager.id)" class="delete-btn">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="!loading && managers.length === 0">暂无管理员数据。</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminManagers',
  data() {
    return {
      managers: [],
      loading: false,
      error: null,
      newManager: {
        username: '',
        password: '',
        phone: '',
        email: '',
      },
    };
  },
  methods: {
    fetchManagers() {
      this.loading = true;
      axios.get('/api/managers')
        .then(res => {
          if (res.data.code !== 200) throw new Error(res.data.message || '获取失败');
          this.managers = res.data.data || [];
        })
        .catch(err => {
          this.error = err.response?.data?.error || err.message;
          this.managers = [];
        })
        .finally(() => {
          this.loading = false;
        });
    },
    addManager() {
      axios.post('/api/managers', this.newManager)
        .then(res => {
          if (res.data.code !== 200) throw new Error(res.data.message || '添加失败');
          alert('添加成功');
          this.newManager = { username: '', password: '', phone: '', email: '' };
          this.fetchManagers();
        })
        .catch(err => {
          alert('添加失败: ' + (err.response?.data?.error || err.message));
        });
    },
    deleteManager(id) {
      if (!confirm('确定删除该管理员吗？')) return;
      axios.delete(`/api/managers/${id}`)
        .then(res => {
          if (res.data.code !== 200) throw new Error(res.data.message || '删除失败');
          alert('删除成功');
          this.fetchManagers();
        })
        .catch(err => {
          alert('删除失败: ' + (err.response?.data?.error || err.message));
        });
    },
  },
  mounted() {
    this.fetchManagers();
  },
};
</script>

<style scoped>
.add-form {
  margin: 10px 0;
}
.add-form input {
  margin-right: 8px;
  padding: 6px;
}
.add-form button {
  padding: 6px 12px;
  background-color: #3498db;
  border: none;
  color: white;
  border-radius: 3px;
  cursor: pointer;
}
.manager-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
.manager-table th,
.manager-table td {
  border: 1px solid #ddd;
  padding: 8px;
}
.manager-table th {
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

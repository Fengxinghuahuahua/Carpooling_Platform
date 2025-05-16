import Mock from 'mockjs';

// 拦截 '/api/auth/login' 请求并返回随机数据
Mock.mock('/api/auth/login', 'post', (options) => {
  
  const { identifier, password } = JSON.parse(options.body);
  
  // 模拟登录逻辑
  if (identifier === 'testuser' && password === '123456') {
    return {
      code: 200,
      message: '登录成功',
      data: {
        token: Mock.Random.guid(), // 随机生成一个 GUID 作为 token
        user: {
          id: Mock.Random.id(),
          name: '测试用户',
          email: 'testuser@example.com',
          avatar: Mock.Random.image('100x100', '#4CAF50', '#FFF', 'Avatar'),
        },
      },
    };
  } else {
    return {
      code: 401,
      message: '用户名或密码错误',
    };
  }
});

// 拦截 '/api/auth/register' 请求并返回随机数据
Mock.mock('/api/auth/register', 'post', (options) => {
  const { name, email, phone, password } = JSON.parse(options.body);

  // 模拟注册逻辑
  if (name && email && phone && password) {
    return {
      code: 200,
      message: '注册成功',
      data: {
        user: {
          id: Mock.Random.id(),
          name,
          email,
          phone,
          avatar: Mock.Random.image('100x100', '#2196F3', '#FFF', 'Avatar'),
        },
      },
    };
  } else {
    return {
      code: 400,
      message: '注册失败，请检查输入信息',
    };
  }
});

const userInfo = {
    username: '拼车达人',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    phone: '13800138000',
    email: 'user@example.com',
    registerTime: '2023-01-15',
    creditScore: 4.7
}

Mock.mock('/api/user/profile', 'get', () => {
    // 模拟获取用户信息
    return {
      code: 200,
      message: '获取用户信息成功',
      data: userInfo
    }
})

Mock.mock('/api/user/update', 'post', (option) => {
    const { username, avatar, phone, email } = JSON.parse(option.body);
    // 模拟更新用户信息
    if (username && avatar && phone && email) {
        userInfo.username = username;
        userInfo.avatar = avatar;
        userInfo.phone = phone;
        userInfo.email = email;
        return {
            code: 200,
            message: '更新用户信息成功',
            data: userInfo
        }
    } else {
        return {
            code: 400,
            message: '更新用户信息失败'
        }
    }
})

let readMessages = [
  {id: 1, title: '欢迎使用拼车平台', time: '2023-06-01 09:00', content: '感谢您注册拼车平台，祝您使用愉快！'},
];

Mock.mock('/api/user/messages/read', 'get', () => {
    // 模拟获取已读消息
    return {
      code: 200,
      message: '获取已读消息成功',
      data: readMessages
    };
})

let unreadMessages = [
  {id: 2, title: '系统通知: 新功能上线', time: '2023-06-13 15:45', content: '我们上线了新的拼车功能，快来体验吧！'},
  {id: 3, title: '您的拼车申请已通过', time: '2023-06-14 10:30', content: '您的拼车申请已通过，请尽快联系车主确认详情。',},
];

Mock.mock('/api/user/messages/unread', 'get', () => {
    // 模拟获取未读消息
    return {
      code: 200,
      message: '获取未读消息成功',
      data: unreadMessages
    };
})

Mock.mock(/\/api\/user\/messages\/read\/(\d+)/, 'post', (options) => {
    const id = options.url.match(/\/api\/user\/messages\/read\/(\d+)/)[1];
    console.log(id)
    const messageIndex = unreadMessages.findIndex(msg => msg.id === parseInt(id));
    if (messageIndex !== -1) {
        const message = unreadMessages.splice(messageIndex, 1)[0];
        readMessages.push(message);
        return {
            code: 200,
            message: '消息已标记为已读',
            data: message
        };
    } else {
        return {
            code: 404,
            message: '消息未找到'
        };
    }
})

Mock.mock('/api/user/joined_carpools', 'get', () => {
    // 模拟获取已加入的拼车信息
    return {
      code: 200,
      message: '获取已加入拼车信息成功',
      data: [
          { id: 1005, origin: '五道口', terminal: '西直门', time: '2023-06-16 09:00', driver: '张师傅', status: '进行中' },
          { id: 987, origin: '天通苑', terminal: '国贸', time: '2023-06-08 07:30', driver: '李女士', status: '已完成' },
      ]
    };
})

Mock.mock('/api/user/initiated_carpools', 'get', () => {
    // 模拟获取已发起的拼车信息
    return {
      code: 200,
      message: '获取已发起拼车信息成功',
      data: [
          { id: 1001, origin: '北京西站', terminal: '中关村', time: '2023-06-15 08:30', seats: 3, status: '进行中' },
          { id: 952, origin: '朝阳公园', terminal: '首都机场', time: '2023-06-10 14:00', seats: 2, status: '已完成' },
          { id: 876, origin: '国贸', terminal: '望京', time: '2023-06-05 18:00', seats: 4, status: '已取消' },
      ]
    };
})

export default Mock;
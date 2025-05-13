import Mock from 'mockjs';

// 拦截 '/api/auth/login' 请求并返回随机数据
Mock.mock('/api/auth/login', 'post', (options) => {
  const { identifier, password } = JSON.parse(options.body);
  console.log('Mock login request:', identifier, password);
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

export default Mock;
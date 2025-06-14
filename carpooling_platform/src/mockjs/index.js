// import Mock from 'mockjs';
// // 拦截 '/api/auth/login' 请求并返回随机数据
// Mock.mock('/api/auth/login', 'post', (options) => {
  
//   const { identifier, password } = JSON.parse(options.body);
  
//   // 模拟登录逻辑
//   if (identifier === 'testuser' && password === '123456') {
//     return {
//       code: 200,
//       message: '登录成功',
//       data: {
//         token: Mock.Random.guid(), // 随机生成一个 GUID 作为 token
//         user: {
//           id: Mock.Random.id(),
//           name: '测试用户',
//           email: 'testuser@example.com',
//           avatar: Mock.Random.image('100x100', '#4CAF50', '#FFF', 'Avatar'),
//         },
//       },
//     };
//   } else {
//     return {
//       code: 401,
//       message: '用户名或密码错误',
//     };
//   }
// });

// // 拦截 '/api/admin/login' 请求并返回随机数据
// Mock.mock('/api/admin/login', 'post', (options) => {
  
//   const { identifier, password } = JSON.parse(options.body);
  
//   // 模拟登录逻辑
//   if (identifier === 'testuser' && password === '123456') {
//     return {
//       code: 200,
//       message: '登录成功',
//       data: {
//         token: Mock.Random.guid(), // 随机生成一个 GUID 作为 token
//         user: {
//           id: Mock.Random.id(),
//           name: '测试用户',
//           email: 'testuser@example.com',
//           avatar: Mock.Random.image('100x100', '#4CAF50', '#FFF', 'Avatar'),
//         },
//       },
//     };
//   } else {
//     return {
//       code: 401,
//       message: '用户名或密码错误',
//     };
//   }
// });



// // 拦截 '/api/auth/register' 请求并返回随机数据
// Mock.mock('/api/auth/register', 'post', (options) => {
//   const { name, email, phone, password } = JSON.parse(options.body);

//   // 模拟注册逻辑
//   if (name && email && phone && password) {
//     return {
//       code: 200,
//       message: '注册成功',
//       data: {
//         user: {
//           id: Mock.Random.id(),
//           name,
//           email,
//           phone,
//           avatar: Mock.Random.image('100x100', '#2196F3', '#FFF', 'Avatar'),
//         },
//       },
//     };
//   } else {
//     return {
//       code: 400,
//       message: '注册失败，请检查输入信息',
//     };
//   }
// });

// const userInfo = {
//     username: '拼车达人',
//     avatar: '',
//     phone: '13800138000',
//     email: 'user@example.com',
//     registerTime: '2023-01-15',
//     creditScore: 4.7
// }

// Mock.mock('/api/user/profile', 'get', () => {
//     // 模拟获取用户信息
//     return {
//       code: 200,
//       message: '获取用户信息成功',
//       data: userInfo
//     }
// })

// Mock.mock("/api/user/upload", "post", (option) => {
//     const file = JSON.parse(option.body);
//     // 模拟文件上传
//     if (file) {
//         return {
//             code: 200,
//             message: '文件上传成功',
//             data: file.data
//         }
//     } else {
//         return {
//             code: 400,
//             message: '文件上传失败'
//         }
//     }
// })

// Mock.mock('/api/user/update', 'post', (option) => {
//     const { username, avatar, phone, email } = JSON.parse(option.body);
//     // 模拟更新用户信息
//     if (username && avatar && phone && email) {
//         userInfo.username = username;
//         userInfo.avatar = avatar;
//         userInfo.phone = phone;
//         userInfo.email = email;
//         return {
//             code: 200,
//             message: '更新用户信息成功',
//             data: userInfo
//         }
//     } else {
//         return {
//             code: 400,
//             message: '更新用户信息失败'
//         }
//     }
// })

// let readMessages = [
//   {id: 1, title: '欢迎使用拼车平台', time: '2023-06-01 09:00', content: '感谢您注册拼车平台，祝您使用愉快！'},
// ];

// Mock.mock('/api/user/messages/read', 'get', () => {
//     // 模拟获取已读消息
//     return {
//       code: 200,
//       message: '获取已读消息成功',
//       data: readMessages
//     };
// })

// let unreadMessages = [
//   {id: 2, title: '系统通知: 新功能上线', time: '2023-06-13 15:45', content: '我们上线了新的拼车功能，快来体验吧！'},
//   {id: 3, title: '您的拼车申请已通过', time: '2023-06-14 10:30', content: '您的拼车申请已通过，请尽快联系车主确认详情。',},
// ];

// Mock.mock('/api/user/messages/unread', 'get', () => {
//     // 模拟获取未读消息
//     return {
//       code: 200,
//       message: '获取未读消息成功',
//       data: unreadMessages
//     };
// })

// Mock.mock(/\/api\/user\/messages\/read\/(\d+)/, 'post', (options) => {
//     const id = options.url.match(/\/api\/user\/messages\/read\/(\d+)/)[1];
//     console.log(id)
//     const messageIndex = unreadMessages.findIndex(msg => msg.id === parseInt(id));
//     if (messageIndex !== -1) {
//         const message = unreadMessages.splice(messageIndex, 1)[0];
//         readMessages.push(message);
//         return {
//             code: 200,
//             message: '消息已标记为已读',
//             data: message
//         };
//     } else {
//         return {
//             code: 404,
//             message: '消息未找到'
//         };
//     }
// })

// Mock.mock('/api/user/joined_carpools', 'get', () => {
//     // 模拟获取已加入的拼车信息
//     return {
//       code: 200,
//       message: '获取已加入拼车信息成功',
//       data: [
//           { id: 1005, origin: '五道口', terminal: '西直门', time: '2023-06-16 09:00', driver: '张师傅', status: '进行中' },
//           { id: 987, origin: '天通苑', terminal: '国贸', time: '2023-06-08 07:30', driver: '李女士', status: '已完成' },
//       ]
//     };
// })

// Mock.mock('/api/user/initiated_carpools', 'get', () => {
//     // 模拟获取已发起的拼车信息
//     return {
//       code: 200,
//       message: '获取已发起拼车信息成功',
//       data: [
//           { id: 1001, origin: '北京西站', terminal: '中关村', time: '2023-06-15 08:30', seats: 3, status: '进行中' },
//           { id: 952, origin: '朝阳公园', terminal: '首都机场', time: '2023-06-10 14:00', seats: 2, status: '已完成' },
//           { id: 876, origin: '国贸', terminal: '望京', time: '2023-06-05 18:00', seats: 4, status: '已取消' },
//       ]
//     };
// })

// // 模拟获取用户列表
// Mock.mock('/api/users', 'get', () => {
//   // 生成10个假用户数据
//   const users = Mock.mock({
//     'users|10': [
//       {
//         'id|+1': 1000,
//         username: '@name',
//         phone: /^1[3456789]\d{9}$/,
//         email: '@email',
//       },
//     ],
//   });
//   return {
//     code: 200,
//     message: '获取用户列表成功',
//     data: users.users,
//   };
// });

// // 模拟删除用户接口
// Mock.mock(/\/api\/users\/\d+/, 'delete', () => {
//   // 这里可以解析 URL 获得 id，不过我们不做实际删除，直接返回成功
//   return {
//     code: 200,
//     message: '用户删除成功',
//   };
// });
// // 模拟当前登录用户 (实际项目中应从登录状态获取)
// // 为了方便测试，我们假设一个用户已登录
// const getCurrentUser = () => {
//   const storedUser = localStorage.getItem('currentUser');
//   if (storedUser) {
//     try {
//       return JSON.parse(storedUser);
//     } catch (e) {
//       // console.error("Error parsing currentUser from localStorage", e);
//       // fallback to a default mock user if parsing fails or no user
//     }
//   }
//   // 如果localStorage中没有，或解析失败，返回一个默认的模拟用户
//   // 或者在登录时将用户信息存入localStorage
//   return {
//     id: 'user001', // 确保这个ID与登录mock返回的ID一致，或在登录时更新
//     name: '测试用户',
//     avatar: Mock.Random.image('50x50', '#FF6347', '#FFF', 'Me'),
//   };
// };


// // 模拟拼车行程数据
// let trips = [
//   {
//     id: Mock.Random.guid(),
//     origin: '辣椒炒肉',
//     destination: '华理轻院',
//     departureTime: '2024/05/31 18:00',
//     publishTime: '2024/05/29 06:14',
//     description: '吃完饭回学校，有一起的没？',
//     seatsTotal: 3,
//     passengers: [], // 存储乘客对象 {id, name, avatar}
//     driver: {
//       id: 'driver001',
//       name: '吴智轩',
//       avatar: Mock.Random.image('50x50', '#4CAF50', '#FFF', '吴'),
//       isDriver: true,
//     },
//     hasCar: true, // 发布者是否提供车辆
//     status: '可拼' // 可拼, 拼满, 已出发, 已取消
//   },
//   {
//     id: Mock.Random.guid(),
//     origin: '平遥古城',
//     destination: '华理轻院',
//     departureTime: '2024/05/31 18:00',
//     publishTime: '2024/05/30 10:00',
//     description: '古城回学校，明天出发，速度!',
//     seatsTotal: 2,
//     passengers: [
//       { id: 'user002', name: '乘客A', avatar: Mock.Random.image('50x50', '#2196F3', '#FFF', 'A') }
//     ],
//     driver: {
//       id: 'driver002',
//       name: '李师傅',
//       avatar: Mock.Random.image('50x50', '#FFC107', '#000', '李'),
//       isDriver: true,
//     },
//     hasCar: true,
//     status: '可拼'
//   },
//   {
//     id: Mock.Random.guid(),
//     origin: '爱琴海购物中心',
//     destination: '华理轻院',
//     departureTime: '2024/06/04 08:00',
//     publishTime: '2024/06/01 12:00',
//     description: '回学校，有一起的吗？',
//     seatsTotal: 1,
//     passengers: [
//        { id: 'user003', name: '乘客B', avatar: Mock.Random.image('50x50', '#9C27B0', '#FFF', 'B') }
//     ],
//     driver: {
//       id: 'driver003',
//       name: '王司机',
//       avatar: Mock.Random.image('50x50', '#E91E63', '#FFF', '王'),
//       isDriver: true,
//     },
//     hasCar: true,
//     status: '拼满'
//   },
//   {
//     id: Mock.Random.guid(),
//     origin: '市中心广场',
//     destination: '科技大学',
//     departureTime: '2024/06/08 22:30',
//     publishTime: '2024/06/02 18:00',
//     description: '周末返校，求同行，可分摊油费。',
//     seatsTotal: 2,
//     passengers: [],
//     driver: {
//       id: 'driver004',
//       name: '赵芳',
//       avatar: Mock.Random.image('50x50', '#00BCD4', '#FFF', '赵'),
//       isDriver: false, // 这个是乘客发起的，找车
//     },
//     hasCar: false,
//     status: '可拼'
//   }
// ];
// // 获取所有行程列表
// Mock.mock('/api/trips', 'get', () => {
//   return {
//     code: 200,
//     message: '获取行程列表成功',
//     data: trips.map(trip => ({
//       ...trip,
//       seatsAvailable: trip.seatsTotal - trip.passengers.length
//     }))
//   };
// });
// // 搜索行程
// Mock.mock('/api/trips/search', 'get', () => {
//   return {
//     code: 200,
//     message: '搜索成功 (返回所有模拟行程)',
//     data: trips
//   }
// });
// // 获取特定行程详情
// Mock.mock(RegExp('/api/trips/[^/]+'), 'get', (options) => {
//   const id = options.url.split('/').pop();
//   const trip = trips.find(t => t.id === id);
//   if (trip) {
//     return {
//       code: 200,
//       message: '获取行程详情成功',
//       data: {
//         ...trip,
//         seatsAvailable: trip.seatsTotal - trip.passengers.length
//       }
//     };
//   } else {
//     return {
//       code: 404,
//       message: '行程未找到'
//     };
//   }
// });

// // 发布新行程
// Mock.mock('/api/trips', 'post', (options) => {

//   const body = JSON.parse(options.body);
//   const currentUser = getCurrentUser(); // 假设发布者是当前用户

//   const newTrip = {
//     id: Mock.Random.guid(),
//     origin: body.origin,
//     destination: body.destination,
//     departureTime: body.departureTime,
//     publishTime: new Date().toLocaleString('sv-SE').replace(' ', ' '),
//     description: body.description,
//     seatsTotal: parseInt(body.seatsTotal, 10),
//     passengers: [],
//     driver: {
//       id: currentUser.id,
//       name: currentUser.name,
//       avatar: currentUser.avatar || Mock.Random.image('50x50', '#FF6347', '#FFF', currentUser.name.charAt(0)),
//       isDriver: body.hasCar,
//     },
//     hasCar: body.hasCar,
//     status: '可拼'
//   };
//   trips.unshift(newTrip); //添加到最前面
//   return {
//     code: 200,
//     message: '行程发布成功',
//     data: newTrip
//   };
// });
// // 加入行程
// Mock.mock(RegExp('/api/trips/[^/]+/join'), 'post', (options) => {
//   const id = options.url.split('/')[3];
//   const trip = trips.find(t => t.id === id);
//   const currentUser = getCurrentUser();

//   if (!trip) {
//     return { code: 404, message: '行程未找到' };
//   }
//   if (trip.passengers.length >= trip.seatsTotal) {
//     return { code: 400, message: '座位已满' };
//   }
//   if (trip.driver.id === currentUser.id) {
//     return { code: 400, message: '您是发起人，不能加入自己的行程' };
//   }
//   if (trip.passengers.some(p => p.id === currentUser.id)) {
//     return { code: 400, message: '您已加入该行程' };
//   }

//   trip.passengers.push({
//     id: currentUser.id,
//     name: currentUser.name,
//     avatar: currentUser.avatar || Mock.Random.image('50x50', '#2196F3', '#FFF', currentUser.name.charAt(0)),
//   });

//   if (trip.passengers.length >= trip.seatsTotal) {
//     trip.status = '拼满';
//   }

//   return {
//     code: 200,
//     message: '加入成功',
//     data: trip
//   };
// });

// // 退出行程
// Mock.mock(RegExp('/api/trips/[^/]+/leave'), 'post', (options) => {
//   const id = options.url.split('/')[3];
//   const trip = trips.find(t => t.id === id);
//   const currentUser = getCurrentUser();

//   if (!trip) {
//     return { code: 404, message: '行程未找到' };
//   }

//   const passengerIndex = trip.passengers.findIndex(p => p.id === currentUser.id);
//   if (passengerIndex === -1) {
//     return { code: 400, message: '您未加入该行程' };
//   }

//   trip.passengers.splice(passengerIndex, 1);
//   if (trip.status === '拼满' && trip.passengers.length < trip.seatsTotal) {
//     trip.status = '可拼';
//   }

//   return {
//     code: 200,
//     message: '退出成功',
//     data: trip
//   };
// });

// // 删除行程 (仅限发起人)
// Mock.mock(RegExp('/api/trips/[^/]+'), 'delete', (options) => {
//   const id = options.url.split('/').pop();
//   const currentUser = getCurrentUser();
//   const tripIndex = trips.findIndex(t => t.id === id);

//   if (tripIndex === -1) {
//     return { code: 404, message: '行程未找到' };
//   }

//   const trip = trips[tripIndex];
//   if (trip.driver.id !== currentUser.id) {
//     return { code: 403, message: '您无权删除此行程' };
//   }

//   trips.splice(tripIndex, 1);
//   return {
//     code: 200,
//     message: '行程删除成功'
//   };
// });

// export default Mock;
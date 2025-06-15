from flask import Flask, request, jsonify, current_app
from flask_login import LoginManager, login_required, current_user, logout_user
from models import db, User, Message
from flask_cors import CORS
from datetime import datetime, timedelta, timezone
import os, base64
import jwt
from sqlalchemy import or_

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/carpool_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

# 初始化扩展
db.init_app(app)
login_manager = LoginManager(app)

@login_manager.request_loader
def load_user_from_request(request):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.query.get(data['user_id'])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, IndexError):

            return None
    return None

# 创建数据库表
with app.app_context():
    db.create_all()

# 注册蓝图
from auth import auth_bp
from trips import travel_bp
from comment import comment_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(travel_bp, url_prefix='/api/trips')
app.register_blueprint(comment_bp, url_prefix='/api/comment')


@app.route('/api/user/logout', methods=['POST'])
@login_required
def logout():
    logout_user() # 清除 flask-login 的用户会话
    return jsonify({'code': 200, 'message': 'Logout successful'})
# ========== 用户管理（管理员用） ==========
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """管理员登录接口"""
    data = request.get_json()
    identifier = data.get('identifier')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({'error': 'Identifier and password are required'}), 400

    user = User.query.filter(or_(User.username == identifier, User.email == identifier)).first()

    if not user or not user.check_password(password) or not user.is_admin:
        return jsonify({'error': 'Invalid admin credentials or not an admin'}), 401

    token = jwt.encode({
        'user_id': user.id,
        'is_admin': True,
        'exp': datetime.now(timezone.utc) + timedelta(hours=8)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({'message': 'Admin login successful', 'token': token})

# ========== 用户管理（管理员用） ==========
@app.route('/api/users', methods=['GET'])
@login_required # 添加登录验证
def get_users():
    """获取所有用户列表（仅限管理员）"""
    if not current_user.is_admin:
        return jsonify({'code': 403, 'message': 'Admin access required'}), 403

    users = User.query.all()
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'username': user.username,
            'phone': user.phone,
            'email': user.email
        })
    return jsonify({'code': 200, 'data': data})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@login_required # 添加登录验证
def delete_user(user_id):
    """删除指定用户（仅限管理员）"""
    if not current_user.is_admin:
        return jsonify({'code': 403, 'message': 'Admin access required'}), 403
    
    if current_user.id == user_id:
        return jsonify({'code': 400, 'message': 'Cannot delete your own admin account'}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'code': 200, 'message': '删除成功'})

# ========== 个人信息 ==========
@app.route('/api/user/profile', methods=['GET'])
@login_required
def get_profile():
    user = current_user

    return jsonify({
        'code': 200,
        'data': {
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'phone': user.phone,
            'email': user.email,
            'registerTime': user.created_at.isoformat(),
            'creditScore': user.credit_score
        }
    })

@app.route('/api/user/update', methods=['POST'])
@login_required
def update_profile():
    data = request.get_json()
    user = current_user
    user.username = data.get('username', user.username)
    user.phone = data.get('phone', user.phone)
    user.email = data.get('email', user.email)
    user.avatar = data.get('avatar', user.avatar)
    db.session.commit()
    return jsonify({'code': 200, 'message': '个人信息已更新'})

@app.route('/api/user/upload', methods=['POST'])
@login_required
def upload_avatar():
    data = request.json.get('data')
    if not data:
        return jsonify({'code': 400, 'message': '没有图片数据'}), 400
    header, encoded = data.split(',', 1)
    file_ext = 'png' if 'png' in header else 'jpg'
    filename = f"user_{current_user.id}_avatar.{file_ext}"
    file_path = os.path.join('static', 'avatars', filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(encoded))
    current_user.avatar = f"/static/avatars/{filename}"
    db.session.commit()
    return jsonify({'code': 200, 'data': current_user.avatar})

# ========== 拼车相关 ==========
@app.route('/api/user/initiated_carpools', methods=['GET'])
@login_required
def get_initiated_carpools():
    print(1)
    travels = current_user.travels
    data = []
    for t in travels:
        data.append({
            'id': t.id,
            'origin': t.departure,
            'terminal': t.destination,
            'time': t.earliest_departure.isoformat(),
            'status': t.status.value if hasattr(t.status, 'value') else t.status
        })
    return jsonify({'code': 200, 'data': data})

@app.route('/api/user/joined_carpools', methods=['GET'])
@login_required
def get_joined_carpools():
    participations = current_user.participations
    data = []
    for p in participations:
        t = p.travel
        data.append({
            'id': t.id,
            'origin': t.departure,
            'terminal': t.destination,
            'time': t.earliest_departure.isoformat(),
            'driver': t.creator.username,
            'status': t.status.value if hasattr(t.status, 'value') else t.status
        })
    return jsonify({'code': 200, 'data': data})

# ========== 消息中心 ==========
@app.route('/api/user/messages/unread', methods=['GET'])
@login_required
def get_unread_messages():
    """获取当前用户的所有未读消息"""
    messages = Message.query.filter_by(recipient_id=current_user.id, is_read=False).order_by(Message.created_at.desc()).all()
    data = [{
        'id': m.id,
        'title': m.title,
        'content': m.content,
        'time': m.created_at.isoformat() # 字段名与前端mock保持一致
    } for m in messages]
    return jsonify({'code': 200, 'data': data})

@app.route('/api/user/messages/read', methods=['GET'])
@login_required
def get_read_messages():
    """获取当前用户的所有已读消息"""
    messages = Message.query.filter_by(recipient_id=current_user.id, is_read=True).order_by(Message.created_at.desc()).all()
    data = [{
        'id': m.id,
        'title': m.title,
        'content': m.content,
        'time': m.created_at.isoformat()
    } for m in messages]
    return jsonify({'code': 200, 'data': data})

@app.route('/api/user/messages/mark_as_read/<int:message_id>', methods=['POST'])
@login_required
def mark_message_as_read(message_id):
    """将单条消息标记为已读"""
    message = Message.query.filter_by(id=message_id, recipient_id=current_user.id).first()

    if not message:
        return jsonify({'code': 404, 'message': 'Message not found or permission denied'}), 404
    
    if message.is_read:
        return jsonify({'code': 200, 'message': 'Message was already marked as read'})

    message.is_read = True
    db.session.commit()
    return jsonify({'code': 200, 'message': 'Message marked as read successfully'})

if __name__ == '__main__':
    app.run(debug=True)
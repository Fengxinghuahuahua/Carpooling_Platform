from flask import Blueprint, request, jsonify
from models import db, User, Captcha
from datetime import datetime, timedelta
import random

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')
    email = data.get('email')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(phone=phone).first():
        return jsonify({'error': 'Phone number already registered'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User(username=username, phone=phone, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # 这里应该返回token或其他认证信息
    return jsonify({'message': 'Login successful', 'user_id': user.id}), 200

@auth_bp.route('/send_captcha', methods=['POST'])
def send_captcha():
    phone = request.json.get('phone')
    if not phone:
        return jsonify({'error': 'Phone number is required'}), 400
    
    # 生成验证码 (实际项目中应该通过短信服务发送)
    code = ''.join(random.choices('0123456789', k=6))
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    
    # 保存验证码
    captcha = Captcha(phone=phone, code=code, expires_at=expires_at)
    db.session.add(captcha)
    db.session.commit()
    
    return jsonify({'message': 'Captcha sent successfully'}), 200

@auth_bp.route('/verify_captcha', methods=['POST'])
def verify_captcha():
    phone = request.json.get('phone')
    code = request.json.get('code')
    
    captcha = Captcha.query.filter_by(phone=phone, code=code).order_by(Captcha.created_at.desc()).first()
    
    if not captcha or captcha.is_expired():
        return jsonify({'error': 'Invalid or expired captcha'}), 400
    
    # 验证成功后可以删除验证码
    db.session.delete(captcha)
    db.session.commit()
    
    return jsonify({'message': 'Captcha verified successfully'}), 200
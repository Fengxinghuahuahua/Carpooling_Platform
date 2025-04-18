from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from enum import Enum

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    avatar = db.Column(db.String(255), default= "http://127.0.0.1:5000/uploads/Profile_Default.png")
    credit_score = db.Column(db.Integer, default=100)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, 
                        default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    
    # 关系
    travels = db.relationship('Travel', backref='creator', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Captcha(db.Model):
    __tablename__ = 'captchas'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime, nullable=False)
    
    def is_expired(self):
        return datetime.now(timezone.utc) > self.expires_at

class TravelStatus(Enum):
    ACTIVE = 'ACTIVE'
    ONGOING = 'ONGOING'
    CANCELED = 'CANCELED'
class Travel(db.Model):
    __tablename__ = 'travels'
    
    id = db.Column(db.Integer, primary_key=True)
    departure = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    earliest_departure = db.Column(db.DateTime, nullable=False)
    latest_departure = db.Column(db.DateTime, nullable=False)
    current_people = db.Column(db.Integer, default=1)
    max_people = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.Enum(TravelStatus), default=TravelStatus.ACTIVE.value)  # active, completed, canceled
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # 外键
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 关系
    comments = db.relationship('Comment', backref='travel', lazy=True)
    participants = db.relationship('TravelParticipant', backref='travel', lazy=True)
    
    def __repr__(self):
        return f'<Travel {self.departure} to {self.destination}>'
class TravelParticipant(db.Model):
    __tablename__ = 'travel_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    travel_id = db.Column(db.Integer, db.ForeignKey('travels.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # 关系
    user = db.relationship('User', backref='participations')
    
    def __repr__(self):
        return f'<TravelParticipant {self.user_id} in {self.travel_id}>'
class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # 外键
    travel_id = db.Column(db.Integer, db.ForeignKey('travels.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment {self.id} by {self.author_id}>'
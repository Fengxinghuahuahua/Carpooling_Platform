from flask import Flask
from flask_login import LoginManager
from models import db, User
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/carpool_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

# 初始化扩展
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 创建数据库表
with app.app_context():
    db.create_all()

# 注册蓝图
from auth import auth_bp
from travel import travel_bp
from comment import comment_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(travel_bp, url_prefix='/travel')
app.register_blueprint(comment_bp, url_prefix='/comment')

if __name__ == '__main__':
    app.run(debug=True)
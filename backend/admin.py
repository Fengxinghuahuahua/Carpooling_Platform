from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# 管理员登录信息（简化处理）
admins = {
    "9201": "admin123"
}

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    admin_id = request.form.get('admin_id')
    password = request.form.get('password')
    if admin_id in admins and admins[admin_id] == password:
        return redirect(url_for('dashboard'))
    return "登录失败，请检查账号或密码", 401

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', users=users)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    global users
    users = [user for user in users if user['id'] != user_id]
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# 模拟数据库（内存存储）
users = [
    {"id": 1000, "name": "Jessica Rodriguez", "phone": "15475498894", "email": "f.fmqov@gysmg.re"},
    {"id": 1001, "name": "Anna Young", "phone": "17774777081", "email": "f.civgfbkaem@kvs.ug"},
    {"id": 1002, "name": "Jason Williams", "phone": "15365187451", "email": "e.lkobzv@yoqooqhpf.中国互联.网络"},
    {"id": 1003, "name": "Elizabeth Walker", "phone": "16465197549", "email": "v.smmxv@shwt.lb"},
    {"id": 1004, "name": "Jennifer Lee", "phone": "13842250233", "email": "t.jtt@txjvixm.sr"},
    {"id": 1005, "name": "Charles Allen", "phone": "16751694213", "email": "s.yfxoyued@kwxtdjdt.ve"},
    {"id": 1006, "name": "John Hall", "phone": "18464122418", "email": "p.ejmbuov@cnlllmd.bs"},
    {"id": 1007, "name": "Jose Wilson", "phone": "18676448352", "email": "v.puj@wbwckabd.td"},
    {"id": 1008, "name": "Richard Anderson", "phone": "19466410523", "email": "o.rjzx@dkef.va"},
    {"id": 1009, "name": "Elizabeth Gonzalez", "phone": "169482569413", "email": "z.jlwcsghb@emroe.cc"}
]

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
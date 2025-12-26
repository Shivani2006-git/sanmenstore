import sqlite3
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='.', static_url_path='')

# Database Setup
DB_NAME = "store.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  email TEXT UNIQUE NOT NULL, 
                  password TEXT NOT NULL,
                  name TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Routes
@app.route('/')
def serve_index():
    return send_from_directory('.', 'login.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# API: Sign Up
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password, name) VALUES (?, ?, ?)", (email, password, name))
        conn.commit()
        conn.close()
        return jsonify({"message": "User created successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "User already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API: Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful", "user": {"id": user[0], "email": user[1], "name": user[3]}}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# API: Get All Products
@app.route('/api/products')
def get_products():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    items = [{"id":r[0], "name":r[1], "price":r[2], "image":r[3], "description":r[4]} for r in c.fetchall()]
    conn.close()
    return jsonify(items)

# API: Get Single Product
@app.route('/api/products/<int:pid>')
def get_product(pid):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id=?", (pid,))
    r = c.fetchone()
    conn.close()
    if r:
        return jsonify({"id":r[0], "name":r[1], "price":r[2], "image":r[3], "description":r[4]})
    else:
        return jsonify({"error":"Not found"}), 404

# API: Admin Get Users
@app.route('/api/admin/users')
def get_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Fetch all details including password as requested
    c.execute("SELECT id, name, email, password FROM users")
    users = [{"id": r[0], "name": r[1], "email": r[2], "password": r[3]} for r in c.fetchall()]
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting Flask server on http://0.0.0.0:{port}")
    # debug=False for production (Render), True for local
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('RENDER') is None)

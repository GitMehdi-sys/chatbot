from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import openai
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Database setup
def init_db():
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Chat history table
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER NOT NULL,
                  role TEXT NOT NULL,
                  message TEXT NOT NULL,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

init_db()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Please login first'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

# API Routes
@app.route('/api/register', methods=['POST'])
def api_register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        hashed_password = generate_password_hash(password)
        
        conn = sqlite3.connect('chatbot.db')
        c = conn.cursor()
        
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                     (username, hashed_password))
            conn.commit()
            return jsonify({'message': 'Registration successful'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Username already exists'}), 400
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        conn = sqlite3.connect('chatbot.db')
        c = conn.cursor()
        
        c.execute('SELECT id, password FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    try:
        user_message = request.json.get('message')
        user_id = session['user_id']
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Save user message to database
        conn = sqlite3.connect('chatbot.db')
        c = conn.cursor()
        c.execute('INSERT INTO chat_history (user_id, role, message) VALUES (?, ?, ?)',
                 (user_id, 'user', user_message))
        conn.commit()
        
        # Get recent chat history for context
        c.execute('''SELECT role, message FROM chat_history 
                    WHERE user_id = ? 
                    ORDER BY timestamp DESC LIMIT 10''', (user_id,))
        history = c.fetchall()
        history.reverse()  # Oldest first
        
        # Build conversation history for OpenAI
        messages = [{"role": row[0], "content": row[1]} for row in history]
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        bot_message = response.choices[0].message.content
        
        # Save bot response to database
        c.execute('INSERT INTO chat_history (user_id, role, message) VALUES (?, ?, ?)',
                 (user_id, 'assistant', bot_message))
        conn.commit()
        conn.close()
        
        return jsonify({
            'response': bot_message,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
@login_required
def api_history():
    try:
        user_id = session['user_id']
        
        conn = sqlite3.connect('chatbot.db')
        c = conn.cursor()
        
        c.execute('''SELECT role, message, timestamp FROM chat_history 
                    WHERE user_id = ? 
                    ORDER BY timestamp ASC''', (user_id,))
        
        history = []
        for row in c.fetchall():
            history.append({
                'role': row[0],
                'message': row[1],
                'timestamp': row[2]
            })
        
        conn.close()
        return jsonify({'history': history}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear-history', methods=['POST'])
@login_required
def api_clear_history():
    try:
        user_id = session['user_id']
        
        conn = sqlite3.connect('chatbot.db')
        c = conn.cursor()
        c.execute('DELETE FROM chat_history WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Chat history cleared'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
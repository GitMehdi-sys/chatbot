# AI Chatbot with Flask & OpenAI

A modern, full-featured AI chatbot with user authentication, chat history, and a clean dark UI.

## ✨ Features

- 🔐 **User Authentication** - Secure login/register system
- 💬 **AI Chat** - Powered by OpenAI GPT-3.5/4
- 📝 **Chat History** - All conversations saved per user
- 🎨 **Modern UI** - Clean dark theme with smooth animations
- 📱 **Responsive** - Works on desktop and mobile
- ⚙️ **Settings** - Clear history and customize preferences
- 🔒 **Secure** - Password hashing with SQLite database

## 📁 Project Structure

```
project/
├── chatbot_app.py          # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys)
├── chatbot.db             # SQLite database (auto-created)
└── templates/
    ├── login.html         # Login page
    ├── register.html      # Registration page
    └── chat.html          # Main chat interface
```

## 🚀 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your API Keys

**OpenAI API Key:**
- Go to https://platform.openai.com
- Sign up/login
- Navigate to API Keys section
- Create new secret key
- Copy the key (starts with `sk-...`)

### 3. Create `.env` File

Create a file named `.env` in the project root:

```env
OPENAI_API_KEY=sk-your-actual-openai-key-here
SECRET_KEY=your-random-secret-key-here
```

**Generate a random SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Run the Application

```bash
python chatbot_app.py
```

The app will run on: **http://localhost:5000**

## 📊 Database Structure

**Location:** `chatbot.db` (SQLite database in project root)

### Tables:

**users**
- `id` - Primary key
- `username` - Unique username
- `password` - Hashed password
- `created_at` - Account creation timestamp

**chat_history**
- `id` - Primary key
- `user_id` - Foreign key to users
- `role` - Either 'user' or 'assistant'
- `message` - Message content
- `timestamp` - Message timestamp

## 🎯 Usage

1. **Register** - Create an account at `/register`
2. **Login** - Sign in at `/login`
3. **Chat** - Start chatting with the AI
4. **History** - All your conversations are saved
5. **Settings** - Clear history or adjust preferences
6. **Logout** - Securely sign out

## 🛠️ Configuration

### Change AI Model

In `chatbot_app.py`, line ~160:

```python
model="gpt-3.5-turbo"  # or "gpt-4" for better responses
```

### Adjust Response Length

```python
max_tokens=500  # Increase for longer responses
```

### Change Temperature (Creativity)

```python
temperature=0.7  # 0.0 = focused, 1.0 = creative
```

## 🔒 Security Features

- ✅ Password hashing with `werkzeug.security`
- ✅ Session-based authentication
- ✅ SQL injection protection (parameterized queries)
- ✅ Environment variables for sensitive data
- ✅ CSRF protection built into Flask

## 🎨 Customization

### Colors

Edit CSS variables in `templates/chat.html`:

```css
:root {
    --bg-primary: #0f0f0f;
    --accent-primary: #00f0ff;
    --accent-secondary: #ff006e;
}
```

### Fonts

Change the Google Font import in all HTML files:

```html
<link href="https://fonts.googleapis.com/css2?family=YOUR+FONT&display=swap">
```

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Redirect to login or chat |
| `/login` | GET | Login page |
| `/register` | GET | Registration page |
| `/chat` | GET | Chat interface (auth required) |
| `/api/register` | POST | Create new account |
| `/api/login` | POST | Authenticate user |
| `/api/logout` | POST | End session |
| `/api/chat` | POST | Send message to AI |
| `/api/history` | GET | Get chat history |
| `/api/clear-history` | POST | Clear user's chat history |

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"
```bash
pip install -r requirements.txt
```

### "OpenAI API key not found"
- Check your `.env` file exists
- Verify the key is correct
- Make sure `python-dotenv` is installed

### "Invalid API key"
- Your OpenAI API key may be expired or invalid
- Generate a new key at https://platform.openai.com

### Database locked error
- Close any other programs accessing `chatbot.db`
- Delete `chatbot.db` and restart (will reset all data)

### Port 5000 already in use
Change the port in `chatbot_app.py`:
```python
app.run(debug=True, port=5001)
```

## 🔐 Important Security Notes

⚠️ **NEVER commit these files to Git:**
- `.env` (contains API keys)
- `chatbot.db` (contains user data)

**Always use `.gitignore`:**
```
.env
chatbot.db
__pycache__/
*.pyc
```

⚠️ **Before deploying to production:**
- Set `debug=False` in `app.run()`
- Use a production WSGI server (gunicorn, uWSGI)
- Enable HTTPS
- Use a production database (PostgreSQL, MySQL)
- Set strong SECRET_KEY
- Enable rate limiting
- Add CORS protection if needed

## 📦 Requirements

- Python 3.7+
- Flask 2.3.3
- OpenAI 0.28.1
- Werkzeug 2.3.7
- python-dotenv 1.0.0

## 📄 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

## 💡 Future Improvements

- [ ] Multiple chat sessions per user
- [ ] Export chat history
- [ ] File upload support
- [ ] Voice input/output
- [ ] Multiple AI models selection
- [ ] Dark/Light theme toggle
- [ ] Markdown rendering in messages
- [ ] Code syntax highlighting
- [ ] Share conversations
- [ ] Admin dashboard

## 📧 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review OpenAI documentation: https://platform.openai.com/docs
3. Check Flask documentation: https://flask.palletsprojects.com/

---

**Made with ❤️ using Flask & OpenAI**
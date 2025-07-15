from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    logout_user, current_user, login_required
)
import os
import bcrypt

# Initialize Flask App
app = Flask(__name__, static_folder='.')
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///users.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Simple Rule-Based Chatbot
def chatbot_response(message):
    message = message.lower()
    if "hello" in message or "hi" in message:
        return "Hello! I'm Baby Masow. How can I help?"
    elif "how are you" in message:
        return "I'm doing great! Thanks for asking."
    elif "bye" in message:
        return "Goodbye! Talk to you soon!"
    else:
        return f"You said: {message}"

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(100))
    chats = db.relationship('Chat', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(500))
    reply = db.Column(db.String(500))

# Create DB Tables
@app.before_request
def create_tables():
    db.create_all()

# Routes
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/about')
@login_required
def about():
    return send_from_directory('.', 'about.html')

@app.route('/login')
def login_page():
    return send_from_directory('.', 'login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    total_chats = Chat.query.filter_by(user_id=current_user.id).count()
    last_chat = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.id.desc()).first()

    return jsonify({
        "email": current_user.email,
        "total_chats": total_chats,
        "last_chat": {
            "message": last_chat.message,
            "reply": last_chat.reply
        } if last_chat else None
    })

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    data = request.json
    user_input = data.get('message')
    response = chatbot_response(user_input)

    new_chat = Chat(user_id=current_user.id, message=user_input, reply=response)
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({"reply": response})

@app.route('/api/history', methods=['GET'])
@login_required
def get_history():
    chats = Chat.query.filter_by(user_id=current_user.id).all()
    history = [{"message": c.message, "reply": c.reply} for c in chats]
    return jsonify(history)

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"success": "User created!"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"success": "Logged in!"})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"success": "Logged out!"})

@app.route('/api/describe-image', methods=['POST'])
def describe_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    file.save("uploaded_image.jpg")

    # For now, return dummy response
    return jsonify({"description": "This is likely a photo or drawing."})

@app.route('/api/websearch', methods=['POST'])
def web_search():
    data = request.json
    query = data.get('query')

    # Dummy response (replace later with SerpAPI)
    return jsonify({
        "answer": f"You asked: '{query}'. I can look that up using a search engine!"
    })

# Run App
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5001)))

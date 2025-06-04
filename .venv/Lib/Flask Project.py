from flask import Flask, render_template, request, jsonify
from discord_webhook import DiscordWebhook
import sqlite3
from datetime import datetime, timedelta
app = Flask(__name__)
DISCORD_WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1352341994864775228/MoipUlv_ykbas0IaOm-VplphwVI3z2eWyKQ6dc6pCIbdPmcvNHLWNixnp0HJOo3sThVf'
# Database helper function
def get_db_connection():
 conn = sqlite3.connect('messages.db')
 conn.row_factory = sqlite3.Row
 return conn
# Database setup
def init_db():
 conn = get_db_connection()
 cursor = conn.cursor()
 cursor.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT,content TEXT NOT NULL,timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
 conn.commit()
 conn.close()
# Function to send message to Discord
def send_to_discord(text):
 webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=text)
 webhook.execute()
# Function to save message to the database
def save_to_database(text):
 conn = get_db_connection()
 cursor = conn.cursor()
 timestamp = datetime.now()
 cursor.execute('INSERT INTO messages (content, timestamp) VALUES (?, ?)', (text, timestamp))
 conn.commit()
 print("Saved message:", text, "at", timestamp)  # Debugging
 conn.close()
# Endpoint 1: Input Text
@app.route('/input_text', methods=['POST'])
def input_text():
    try:
        data = request.form.get('text')  # Input text from HTML form
        if not data or not isinstance(data, str):
            return jsonify({"status": "error", "message":"Invalid input"}), 400
         # Send message to Discord and save it to database
        send_to_discord(data)
        save_to_database(data)
        return jsonify({"status": "success", "message": "Message sent successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
# Endpoint 2: Message Retrieval
@app.route('/get_messages', methods=['GET'])
def get_messages():
    try:
        cutoff_time = datetime.now() - timedelta(minutes=30)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT content, timestamp FROM messages WHERE timestamp > ?', (cutoff_time,))
        messages = cursor.fetchall()
        conn.close()
        # Debugging: print fetched messages
        print("Retrieved messages:", messages)
        return jsonify({"status": "success", "messages":[{"content": row['content'], "timestamp": row['timestamp']}
for row in messages]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint 3: Serve HTML Page
@app.route('/')
def index():
    return render_template('index.html')


# Initialize database and run the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

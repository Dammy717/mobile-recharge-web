from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'recharge.db'

# ---------- DATABASE SETUP ----------
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            service TEXT,
            amount TEXT,
            phone TEXT,
            decoder TEXT,
            platform TEXT
        )''')
        db.commit()

# ---------- ROUTES ----------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        user = session.get('user', 'guest')
        service = request.form.get('service')
        amount = request.form.get('amount')
        phone = request.form.get('phone')
        decoder = request.form.get('decoder')
        platform = request.form.get('platform')

        db = get_db()
        db.execute("INSERT INTO history (user, service, amount, phone, decoder, platform) VALUES (?, ?, ?, ?, ?, ?)",
                   (user, service, amount, phone, decoder, platform))
        db.commit()

        if service == 'data':
            return f"You bought {amount}MB of data."
        elif service == 'airtime':
            return f"You recharged ₦{amount} airtime."
        elif service == 'betting':
            return f"Funded ₦{amount} to {platform} (Phone: {phone})"
        elif service == 'cable':
            return f"Paid ₦{amount} to {platform} (Decoder ID: {decoder})"
        else:
            return "Invalid selection."

@app.route('/history')
def history():
    user = session.get('user', 'guest')
    db = get_db()
    cur = db.execute("SELECT * FROM history WHERE user = ?", (user,))
    records = cur.fetchall()
    return render_template('history.html', records=records)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['user'] = username
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# ---------- RUN ----------
if __name__ == '_main_':
    init_db()
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 5000), debug=True)
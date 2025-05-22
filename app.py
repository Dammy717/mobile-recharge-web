from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    service = request.form['service']
    amount = request.form['amount']
    phone = request.form.get('phone', '')
    decoder = request.form.get('decoder', '')
    platform = request.form.get('platform', '')

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

if __name__ == "__main__":
    app.run(debug=True)
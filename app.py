from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    return render_template('index.html')

@app.route('/submit', methods=["POST"])
def submit():
    service = request.form.get('service')
    amount = request.form.get('amount')
    phone = request.form.get('phone')
    decoder = request.form.get('decoder')
    platform = request.form.get('platform')

    if service == 'data':
        message = f"You bought {amount}MB of data."
    elif service == 'airtime':
        message = f"You recharged ₦{amount} airtime."
    elif service == 'betting':
        message = f"Funded ₦{amount} to {platform} (Phone: {phone})"
    elif service == 'cable':
        message = f"Paid ₦{amount} to {platform} (Decoder ID: {decoder})"
    else:
        message = "Invalid selection."

    return render_template("success.html", message=message)

if __name__ == '_main_':
    app.run(host="0.0.0.0", port=5000, debug=True)
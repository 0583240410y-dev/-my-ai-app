import os
import stripe
from flask import Flask, request, jsonify, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# הגדרת בסיס נתונים SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# הגדרת מפתחות סליקה
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "YOUR_STRIPE_SECRET_KEY")
ENDPOINT_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "YOUR_WEBHOOK_SECRET_KEY")

# מודל משתמש
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_subscriber = db.Column(db.Boolean, default=False)
    subscription_id = db.Column(db.String(120), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "<h1>ברוכים הבאים לאפליקציית ה-AI שלך!</h1><p>המערכת באוויר ומחוברת בהצלחה.</p>"

@app.route('/create-checkout', methods=['POST'])
def create_checkout():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'ils',
                    'product_data': {'name': 'מנוי חודשי לבוט AI'},
                    'unit_amount': 4900,
                    'recurring': {'interval': 'month'},
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.host_url + 'success',
            cancel_url=request.host_url + 'cancel',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e), 400

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, ENDPOINT_SECRET)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_email') or session.get('customer_details', {}).get('email')
        sub_id = session.get('subscription')
        
        user = User.query.filter_by(email=customer_email).first()
        if user:
            user.is_subscriber = True
            user.subscription_id = sub_id
        else:
            new_user = User(email=customer_email, is_subscriber=True, subscription_id=sub_id)
            db.session.add(new_user)
        db.session.commit()

    return jsonify({'status': 'success'}), 200

@app.route('/success')
def success():
    return "<h2>התשלום בוצע בהצלחה! המנוי שלך הופעל.</h2>"

@app.route('/cancel')
def cancel():
    return "<h2>התשלום בוטל.</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

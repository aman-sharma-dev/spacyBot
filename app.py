from flask import Flask, render_template, request, jsonify, session
from flask_mail import Mail, Message
import openai
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import ssl
from urllib.parse import quote 
 
openai.api_key = 'your API code'

app = Flask(__name__)
app.secret_key = 'zZIZC6ZUxbqQWE8qIGSf'
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["86400 per day", "3600 per hour"],
    storage_uri="memory://"
) 
 
password = 'Bareilly@123'
encoded_password = quote(password)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{encoded_password}@localhost/users'
app.config['MIME_TYPES'] = {
    '.js': 'application/javascript',
    '.ts': 'application/typescript'
}
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'amansharma.devloper@gmail.com'
app.config['MAIL_PASSWORD'] = 'apbp lbhb wncr wcue'
app.config['MAIL_DEFAULT_SENDER'] = 'amansharma22102004@gmail.com'
mail = Mail(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15))
    user_input = db.Column(db.String(855))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
class newuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
@app.route("/")
def index():
    user_ip = request.remote_addr
    session['user_ip'] = user_ip

    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('text')
    
    if user_input is not None and "name" in user_input.lower() and "email" in user_input.lower():
        name_start = user_input.lower().find("name") + 6
        email_start = user_input.lower().find("email")
        name = user_input[name_start:email_start].strip()
        email = user_input[email_start:].strip()

        entry = newuser(name=name, email=email)
        db.session.add(entry)
        db.session.commit()

        user_ip = session.get('user_ip', None)
        session['user_name'] = name  
        session['user_email'] = email  
        send_email(user_ip, user_input, name, email)

        return jsonify({"success": True})
    else:
        return jsonify({"error": "Invalid input"}), 400

@app.route("/get", methods=["GET", "POST"])
def Uchat():
    msg = request.form["msg"]
    input = msg

    user_session = session.get('user_session', {'user_input': None})
    user_session['user_input'] = input
    session['user_session'] = user_session
    user_ip = session.get('user_ip', None)
    user_input = user_session.get('user_input', None)
    name = session.get('user_name')  
    email = session.get('user_email')

    if user_ip and user_input and name and email:
        user = User(ip_address=user_ip, user_input=user_input)
        db.session.add(user)
        db.session.commit()

    response = generate_answer(user_session['user_input'])

    send_email(user_ip, user_input, name, email)

    return generate_answer(input)

def generate_answer(text):
    max_tokens = 700
    input_chunks = [text[i:i + max_tokens] for i in range(0, len(text), max_tokens)]

    responses = []

    for chunk in input_chunks:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "your name is luna you are a sales assistent of salesharbor, salesharbor website is salesharbor.io and salesharbor is formed in 2023, generate brief answers if The user expresses a desire to schedule a call with the sales team. Luna assures the user that a team member will contact them to arrange the call. When inquiring about pricing, Luna mentions that a team member will provide detailed information during a scheduled call. In response to the user's question about services, Luna outlines two offerings: Appointment Setting and Sales Consultancy, detailing the features of the Appointment Setting service. The user asks about the timeline for seeing results, and Luna explains the process, emphasizing that results start from Month 1. Regarding team assignment, Luna assures the user of a dedicated account manager and describes the internal collaboration involving data miners, copywriters, and outreach specialists. Luna also explains the monthly email volume will be ranging from 8000 to 22000, dependent on the chosen plan, and mentions a forthcoming call to discuss these plans. The user inquires about the commitment period, and Luna offers a risk-free trial of 3 months with a pay-per-lead option, transitioning to a monthly retainer afterward. Luna elaborates on lead sourcing, detailing the use of platforms like LinkedIn and ZoomInfo and the meticulous validation process, emphasizing the delivery of tailored, high-quality leads aligned with the user's goals.The headquarters of Salesharbor is in Amsterdam in the Netherlands.If user ask about SalesHarbor then Luna should respond SalesHarbor, with over two decades of expertise in sales and lead generation, excels in connecting businesses with ideal clients for strategic growth. Founded on the fusion of art and science, our commitment to excellence is built on a solid 20-year foundation. If a user asks a question that is not related to Sales Harbor or sales and marketing,If user ask about SalesHarbor then reply, Luna will respond by asking, 'Do you have any specific questions about SalesHarbor?"},
                {"role": "user", "content": chunk}
            ]
        )
        responses.append(response['choices'][0]['message']['content'].strip())
        answer = ' '.join(responses)
        return answer
def send_email(user_ip, user_input, name, email):
    subject = f'User Input Log for {name} - Email: {email}'
    body = f"User IP: {user_ip}\nUser Input: {user_input}\nTimestamp: {datetime.utcnow()}\nUser Name: {name}\nUser Email: {email}"
    recipients = ['amansharma22102004@gmail.com','mona.juneja@salesharbor.io']

    msg = Message(subject=subject, body=body, recipients=recipients)

    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

ssl_certificate_path = '/etc/nginx/ssl-certificates/bot1.salesharbor.io.crt'
ssl_private_key_path = '/etc/nginx/ssl-certificates/bot1.salesharbor.io.key'

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile=ssl_certificate_path, keyfile=ssl_private_key_path)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    try:
        app.secret_key = 'zZIZC6ZUxbqQWE8qIGSf'
        app.run(host='0.0.0.0', port='443', debug=True, ssl_context=ssl_context)
    except Exception as e:
        print(f"Error starting the application: {e}")

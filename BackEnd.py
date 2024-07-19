from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import random
import threading
import time
import nexmo

app = Flask(__name__)
app.secret_key = '#mhme@aih'  # Needed for session management
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'agrigo'  # Correct parameter name ( MySQL_DB )
mysql = MySQL(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mohammedyousuf432003@gmail.com'
app.config['MAIL_PASSWORD'] = 'tahb pbyc aacy wcxu'
mail = Mail(app)

client = nexmo.Client(key="#mhme@aih", secret="###")

@app.route("/")
def HomePage():
    return render_template("HomePage.html")

@app.route("/LoginPage", methods=['GET','POST'])
def LoginPage():
    return render_template()
 
@app.route("/logout")
def logout():
    return render_template()

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template()


def send_email(to_email):
    subject = "Password Reset Request"
    body = "This is a custom email for password reset. New Otp = "
    attachment_opt = otp

    msg = Message(subject, sender="mohammedyousuf432003@gmail.com", recipients=[to_email])
    msg.body = body + attachment_opt

    try:
        mail.send(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        flash(f"Failed to send email: {e}", 'error')
        
def send_sms(to_sms, otp):
    body = f"This is a custom message for password reset. Your OTP is: {otp}"

    try:
        response = client.send_message({
            "from": "Nexmo",
            "to": to_sms,
            "text": body
        })
        if response['messages'][0]['status'] == '0':
            print("SMS sent successfully!")
        else:
            print(f"Failed to send SMS: {response['messages'][0]['error-text']}")
            flash(f"Failed to send SMS: {response['messages'][0]['error-text']}", 'error')
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        flash(f"Failed to send SMS: {e}", 'error') 
    
otp = None

def generate_otp():
    """Generates a 6-digit OTP and assigns it to the global variable otp."""
    global otp
    otp = f"{random.randint(100000, 999999)}"
    print(f"Generated OTP: {otp}")  # For debugging

def update_otp_every_5_minutes():
    """Updates the OTP every 5 minutes."""
    while True:
        generate_otp()
        time.sleep(300)  # Sleep for 5 minutes

# Start the OTP update in a separate thread
otp_update_thread = threading.Thread(target=update_otp_every_5_minutes)
otp_update_thread.daemon = True  # Daemonize thread
otp_update_thread.start()

@app.route('/otp_validation', methods=['GET', 'POST'])
def otp_validation():
    return render_template()

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    return render_template()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template()
   

@app.route('/connection')
def connection():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("select * from users")
    output = cur.fetchall()
    return str(output)

if __name__ == '__main__':
    app.run(port=2585, host="0.0.0.0", debug=True)
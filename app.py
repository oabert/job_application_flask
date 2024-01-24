from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

from datetime import datetime
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('SENDER')
app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')

db = SQLAlchemy(app)

mail = Mail(app)


class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    start_date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route('/', methods=['GET', 'POST'])
def index_html():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        start_date = request.form['start_date']
        date = datetime.strptime(start_date, '%Y-%m-%d')
        occupation = request.form['occupation']

        form = FormData(first_name=first_name, last_name=last_name, email=email, start_date=date,
                        occupation=occupation)
        db.session.add(form)
        db.session.commit()

        message_body = f'Thank you for your submission, {first_name}. \n' \
                       f'Here your data:\n {first_name}\n{last_name}\n{date}\n' \
                       f'Have a great day'
        message = Message(subject='New job app form submission',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[email],
                          body=message_body)

        mail.send(message)

        flash('Your application was submitted successfully!', 'success')

        return redirect(url_for("index_html"))
    return render_template('index.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)

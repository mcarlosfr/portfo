import os
from flask import Flask, render_template, url_for, request, redirect
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path # like os.path
import datetime
import csv
# cd 'C:\Users\micki\Documents\Python Scripts\scripting\web_server\'
# use "Set-ExecutionPolicy Unrestricted -Scope Process" to be able to activate the web server
# .\\Scripts\activate.ps1
# $env:FLASK_APP = "hello.py"
# $env:FLASK_ENV = "development"
# flask run

app = Flask(__name__)
print(__name__)




@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>.html')
def pages(page_name = None):
    return render_template(f'{page_name}.html')

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
	if request.method == 'POST':
		try:
			data = request.form.to_dict()
			write_to_file(data)
			write_to_csv(data)
			send_email(data)
			return redirect('/thankyou.html')
		except Exception as inst:
			return inst
	else:
		return 'Something went wrong. Try again!'
    # return 'form submitted hourrahhh'







def write_to_file(data):
	with open('database.txt', mode='a') as database:
		email = data['email']
		subject = data['subject']
		message = data['message']
		email_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		file = database.write(f'\n {email},{subject},{message},{email_time}')


def write_to_csv(data):
	with open('database.csv', mode='a', newline='') as database2:
		email = data['email']
		subject = data['subject']
		message = data['message']
		email_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		csv_writer = csv.writer(database2, delimiter = ',', quotechar='"',quoting = csv.QUOTE_MINIMAL)
		csv_writer.writerow([email,subject,message,email_time])


def send_email(data):
	email_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
	email = EmailMessage()
	email['from'] = 'mcarlos-toulouse@outlook.fr'
	email['to'] = 'mcarlos-toulouse@outlook.fr'
	email['subject'] = 'Contact from the portfolio from : '+ data['email'] + ' for : ' + data['subject'] + ' at ' + email_time
	email.set_content(data['message'])
	with smtplib.SMTP(host = 'smtp-mail.outlook.com', port=587) as smtp:
		smtp.ehlo()
		smtp.starttls()
		smtp.login('mcarlos-toulouse@outlook.fr','%S3Danybil.1.%23072016')
		smtp.send_message(email)
		print('email sent')
# @app.route('/index.html')
# def my_home():
#     return render_template('index.html')

    
# @app.route('/index.html')
# def my_home():
#     return render_template('index.html')


# @app.route('/<username>')
# def hello_user(username = None):
#     return render_template('user_index.html', name=username)

# @app.route('/about.html')
# def about():
#     return render_template('about.html')


# @app.route('/')
# def hello_world():
#     return 'Hello, World! \n Here is Aroi HAHAHAHAHA'

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

# @app.route('/blog')
# def blog():
#     return 'This is my blog'

# @app.route('/blog/2020/dogs')
# def blog2():
#     return 'This is my dog'
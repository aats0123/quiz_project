import smtplib, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send_email(details, email_address):
    today = datetime.now()
    subject = "Quizee - тест по {} от {}".format(details['subject'], details['teacher'], format_spec='utf-8')
    from_address = 'quizee@quizee.com'
    allowed_addresses = ['smtp.mailer.box@gmail.com', 'gosh.peshev@gmail.com']
    if email_address in allowed_addresses:
        body_text = ''''
                Имате зададен тест {} по {} от {}.
                Последвате линка за да отговорите {}
            
                '''.format(details['title'], details['subject'], details['teacher'], details['link'],
                           format_spec='utf-8')
        body = subject + ':\n' + body_text
        to = email_address
        gmail_user = 'new.smtp.emailer@gmail.com'
        gmail_password = 'Why Gosho?'
        email = """
        From: {}
        To: {}
        Subject: {}

        {}

        """.format(from_address, to, subject, body)
        msg = MIMEMultipart()
        msg['FROM'] = from_address
        msg['To'] = to
        msg['Subject'] = subject
        text = MIMEText(email)
        msg.attach(text)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(from_address, to, msg.as_string())
            server.close()
            print('Email sent!')
        except Exception as e:
            print(str(e))

# subject = "Домашна работа по математика за {}-{}-{}".format(today.day, today.month, today.year, format_spec='utf-8')
# from_address = 'bad.dad@mail.com'
# to = ['sonia.tsenova@gmail.com', 'tsenova.d@gmail.com', 'naskots@gmail.com']

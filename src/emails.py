import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "g.j.kaye@cs.bham.ac.uk"
receiver_email = "georgejkaye@gmail.com"

message = MIMEMultipart("alternative")
message["Subject"] = "Test"
message["From"] = sender_email
message["To"] = receiver_email
text = MIMEText("Hello!", "plain")
message.attach(text)

port = 465

with open("credentials") as credentials:
    password = credentials.readline()

context = ssl.create_default_context()
with smtplib.SMTP_SSL("auth-smtp.bham.ac.uk", port, context=context) as server:
    server.login("gjk591", password)
    server.sendmail(sender_email, receiver_email, message.as_string())

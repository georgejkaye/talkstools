import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader, select_autoescape


def write_email(config, talk):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("upcoming_talk.txt")
    email = template.render(
        talk=talk, room=config["room"], zoom=config["zoom"], admin=config["admin"], page=config["page"])
    return email


def send_email(config, talk, email):

    email_sender = config["sender_email"]
    email_recipient = config["recipient_email"]
    smtp_host = config["smtp"]["host"]
    smtp_port = config["smtp"]["port"]
    smtp_user = config["smtp"]["user"]
    smtp_password = config["smtp"]["password"]

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Talk by { talk.speaker }: { talk.datetime.get_short_string() }"
    message["From"] = email_sender
    message["To"] = email_recipient
    text = MIMEText(email, "plain")
    message.attach(text)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(email_sender, email_recipient, message.as_string())

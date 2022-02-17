from debug import debug
import smtplib
import ssl
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader, select_autoescape
from textwrap import wrap
from config import ABSTRACT, REMINDER


def write_email(config, template, talk):

    current_dir = Path(__file__).resolve().parent
    templates_dir = current_dir / "templates"

    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template(template)
    email = template.render(config=config, talk=talk)
    return email


def send_email(config, talk, email, mode):

    email_sender = config.sender_email

    if mode == ABSTRACT:
        email_recipient = talk.email
        email_cc = None
    else:
        email_recipient = config.recipient_email
        email_cc = talk.email

    smtp_host = config.smtp.host
    smtp_port = config.smtp.port
    smtp_user = config.smtp.user
    smtp_password = config.smtp.password

    message = MIMEMultipart("alternative")

    if mode == ABSTRACT:
        subject = f"Your upcoming Bravo talk, { talk.get_short_datetime() }"
    else:
        subject = f"Talk by { talk.speaker }, { talk.get_short_datetime() }"
        if mode == REMINDER:
            subject = f"Reminder: " + subject

    message["Subject"] = subject

    message["From"] = email_sender
    message["To"] = email_recipient
    if email_cc is not None:
        message["Cc"] = email_cc
    text = MIMEText(email, "plain")
    message.attach(text)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
        try:
            server.login(smtp_user, smtp_password)
        except Exception as e:
            debug(config,
                  f"Error logging into server {smtp_host}:{smtp_port} as user {smtp_user}: {e.smtp_code} {e.smtp_error.decode('UTF-8')}")
            exit(1)

        try:
            server.sendmail(email_sender, email_recipient, message.as_string())
        except Exception as e:
            debug(config,
                  f"Error sending email from server {smtp_host}:{smtp_port} as user {smtp_user}: {e.smtp_code} {e.smtp_error.decode('UTF-8')}")
            exit(1)

    debug(config, f"Sent email to {email_recipient}")

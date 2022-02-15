import smtplib
import ssl
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader, select_autoescape
from scraper import get_talks_page
from debug import debug


class ZoomDetails:
    def __init__(self, link, id, password):
        self.link = link
        self.id = id
        self.password = password


class AdminDetails:
    def __init__(self, name, email):
        self.name = name
        self.email = email


def write_email(config, template, talk):

    current_dir = Path(__file__).resolve().parent
    templates_dir = current_dir / "templates"

    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"])
    )

    zoom = ZoomDetails(config["zoom"]["link"],
                       config["zoom"]["id"], config["zoom"]["password"])
    admin = AdminDetails(config["admin"]["name"], config["admin"]["email"])

    template = env.get_template(template)
    email = template.render(
        talk=talk, room=config["room"], zoom=zoom, admin=admin, page=get_talks_page(config["talks_id"]))
    return email


def send_email(config, log_file, talk, email):

    email_sender = config["sender_email"]
    email_recipient = config["recipient_email"]
    smtp_host = config["smtp"]["host"]
    smtp_port = config["smtp"]["port"]
    smtp_user = config["smtp"]["user"]
    smtp_password = config["smtp"]["password"]

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Talk by { talk.speaker }: { talk.get_short_datetime() }"
    message["From"] = email_sender
    message["To"] = email_recipient
    text = MIMEText(email, "plain")
    message.attach(text)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
        try:
            server.login(smtp_user, smtp_password)
        except Exception as e:
            debug(log_file,
                  f"Error logging into server {smtp_host}:{smtp_port} as user {smtp_user}: {e.smtp_code} {e.smtp_error.decode('UTF-8')}")
            exit(1)

        try:
            server.sendmail(email_sender, email_recipient, message.as_string())
        except Exception as e:
            debug(log_file,
                  f"Error sending email from server {smtp_host}:{smtp_port} as user {smtp_user}: {e.smtp_code} {e.smtp_error.decode('UTF-8')}")
            exit(1)

    debug(log_file, f"Sent email to {email_recipient}")

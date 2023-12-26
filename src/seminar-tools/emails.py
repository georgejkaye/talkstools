import subprocess
from debug import debug
import smtplib
import ssl
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader, select_autoescape


def write_and_send_email(config, seminar, talk, template, is_reminder, stdout):
    email = write_email(config, seminar, talk, template)
    if stdout:
        print("\n==============================================\n")
        print(email)
        print("\n==============================================\n")
    else:
        send_email(config, seminar, talk, email, is_reminder)


def write_email(config, seminar, talk, template):
    current_dir = Path(__file__).resolve().parent
    templates_dir = current_dir / "templates"

    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = env.get_template(template)
    email = template.render(config=config, seminar=seminar, talk=talk)
    return email


def prepare_email(config, seminar, talk, body) -> None:
    to_item = f"to='{seminar.mailing_list}'"
    from_item = f"from={config.admin.email}"
    subject_item = f"subject='{ talk.series } talk by { talk.speaker }, { talk.get_short_datetime() }'"
    body_item = f"body='{body}'"
    plain_text_item = "format=2"
    compose_items = ",".join(
        [to_item, from_item, subject_item, body_item, plain_text_item]
    )
    quoted_compose_items = f'"{compose_items}"'
    command = f"thunderbird -compose {quoted_compose_items}"
    subprocess.Popen(command, shell=True)


def send_email(config, seminar, talk, email_content, is_reminder):
    email_sender = config.admin.email
    email_recipient = seminar.mailing_list

    if email_recipient is not None:
        smtp_host = config.smtp.host
        smtp_port = config.smtp.port
        smtp_user = config.smtp.user
        smtp_password = config.smtp.password

        message = MIMEMultipart("alternative")

        subject = (
            f"{ talk.series } talk by { talk.speaker }, { talk.get_short_datetime() }"
        )
        if is_reminder:
            subject = f"Reminder: " + subject

        message["Subject"] = subject

        message["From"] = email_sender
        message["To"] = email_recipient
        text = MIMEText(email_content, "plain")
        message.attach(text)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
            try:
                server.login(smtp_user, smtp_password)
            except Exception as e:
                debug(
                    config,
                    f"Error logging into server {smtp_host}:{smtp_port} as user {smtp_user}: {e.smtp_code} {e.smtp_error.decode('UTF-8')}",
                )
                exit(1)

            try:
                server.sendmail(email_sender, email_recipient, message.as_string())
            except Exception as e:
                debug(
                    config,
                    f"Error sending email from server {smtp_host}:{smtp_port} as user {smtp_user}: {e.smtp_code} {e.smtp_error.decode('UTF-8')}",
                )
                exit(1)

        debug(config, f"Sent email to {email_recipient}")

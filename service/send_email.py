import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EmailConfig


def send_email(recipients, subject, body, html=None):
    PORT_LIST = (25, 587, 465)

    FROM = EmailConfig.FROM
    TO = recipients if isinstance(recipients, (list, tuple)) else [recipients]
    SUBJECT = subject
    TEXT = body
    HTML = html

    if not html:
        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    else:
                # https://stackoverflow.com/questions/882712/sending-html-email-using-python#882770
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        msg['From'] = FROM
        msg['To'] = ", ".join(TO)

        # Record the MIME types of both parts - text/plain and text/html.
        # utf-8 -> https://stackoverflow.com/questions/5910104/python-how-to-send-utf-8-e-mail#5910530
        part1 = MIMEText(TEXT, 'plain', "utf-8")
        part2 = MIMEText(HTML, 'html', "utf-8")

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        message = msg.as_string()


    try:
        if EmailConfig.PORT not in PORT_LIST:
            raise Exception("Port %s not one of %s" % (EmailConfig.PORT, PORT_LIST))

        if EmailConfig.PORT in (465,):
            server = smtplib.SMTP_SSL(EmailConfig.HOST, EmailConfig.PORT)
        else:
            server = smtplib.SMTP(EmailConfig.HOST, EmailConfig.PORT)

        # optional
        server.ehlo()

        if EmailConfig.PORT in (587,):
            server.starttls()

        server.login(EmailConfig.USER, EmailConfig.PWD)
        server.sendmail(FROM, TO, message)
        server.close()
        # logger.info("SENT_EMAIL to %s: %s" % (recipients, subject))
    except Exception as ex:
        return ex
    return None

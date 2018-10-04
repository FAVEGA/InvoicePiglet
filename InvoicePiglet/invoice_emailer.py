import logging
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from InvoicePiglet.settings import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def email_invoice(invoice, pdf_file):
    msg = MIMEMultipart()
    msg['Subject'] = "Factura {}-{}".format(invoice['series'], invoice['number'])
    msg['From'] = 'Facturacion FAVEGA <billing@favega.com>'
    msg['To'] = invoice['customer_email']
    msg['Reply-To'] = 'FAVEGA(Roberto) <roberto@favega.com>'
    msg.preamble = 'Multipart message.\n'

    part = MIMEText(
        'Estimado {},\n\n'
        'Adjunta le enviamos la factura {}-{}.\n'
        'Para cualquier duda, contacte con nosotros.\n\n'
        'Un saludo,\n\n'
        'FAVEGA EQUIPAMIENTOS S.L.\n'
        'Ctra Logroño Km 247\n'
        '50011 ZARAGOZA\n'
        '976 77 18 65\n'
            .format(invoice['customer_name'], invoice['series'], invoice['number'])
    )
    msg.attach(part)
    part = MIMEApplication(open(pdf_file, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=os.path.split(pdf_file)[-1])
    msg.attach(part)
    try:
        s = smtplib.SMTP(SMTP_SERVER, port=SMTP_PORT)
        s.debuglevel = 1
        s.starttls()
        s.login(SMTP_USER, SMTP_PASSWORD)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
    except smtplib.SMTPException as e:
        logger.error("Error sending email to %s", invoice['customer_email'], e)
    else:
        logger.info("Successfully sent email to %s", invoice['customer_email'])

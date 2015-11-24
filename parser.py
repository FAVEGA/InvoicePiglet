# coding=utf-8
import logging
import re
import smtplib
import subprocess
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import errno
from jinja2 import Environment, FileSystemLoader

from settings import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('InvoicePiglet')
logger.setLevel(logging.INFO)


class InvoiceParser(object):
    def parse_invoices(self, input_string):
        invoice_strings = self.split_input_string(input_string)
        invoices = []
        for invoice in invoice_strings:
            invoices.append(self.parse_single_invoice(invoice))
        return invoices

    def parse_single_invoice(self, invoice_string):
        invoice = {}
        for (field, regex) in INVOICE_REGEXES:
            invoice[field] = self.get_sanitized_regex_group(regex, invoice_string)
        invoice['products'] = self.parse_products(invoice_string)
        return invoice

    def parse_products(self, invoice_string):
        products = []
        for match in re.findall(PRODUCT_REGEX, invoice_string):
            product = {'description': self.escape_latex(match[0].strip()),
                       'amount': self.escape_latex(match[1].strip()), 'price': self.escape_latex(match[2].strip()),
                       'discount': self.escape_latex(match[3].strip()),
                       'discounted_price': self.escape_latex(match[4].strip())}
            products.append(product)
        return products

    def get_sanitized_regex_group(self, regex, string):
        return self.escape_latex(re.search(regex, string).group(1).strip())

    @staticmethod
    def split_input_string(input_string):
        return [s for s in input_string.split('<DOC.INI>') if s]

    @staticmethod
    def escape_latex(string):
        for (character, escape) in LATEX_ESCAPES:
            string = string.replace(character, escape)
        return string


class InvoiceRenderer(object):
    def __init__(self):
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
        self.template = env.get_template('invoice.tex.j2')

    def render_invoice(self, invoice):
        return self.template.render(invoice)


class LatexToPdfConverter(object):
    @staticmethod
    def export(latex, pdf_file_location):
        temp_file = pdf_file_location.replace('.pdf', '.tex')
        with open(temp_file, 'w', encoding='utf-8') as tf:
            tf.write(latex)

        command = ['pdflatex', temp_file, '-enable-installer', '-output-directory',
                   os.path.dirname(pdf_file_location)]
        logger.info("Executing", " ".join(command))

        FNULL = open(os.devnull, 'w')
        subprocess.call(command, shell=True, stdout=FNULL, stderr=FNULL)
        os.remove(temp_file)
        os.remove(temp_file.replace('.tex', '.aux'))
        os.remove(temp_file.replace('.tex', '.log'))


class InvoiceEmailer(object):
    @staticmethod
    def send_invoice(invoice, pdf_file):
        msg = MIMEMultipart()
        msg['Subject'] = "Factura {}-{}".format(invoice['series'], invoice['number'])
        msg['From'] = 'Facturacion FAVEGA <billing@favega.com>'
        msg['To'] = invoice['customer_email']
        msg['Reply-To'] = 'FAVEGA(Roberto) <roberto@favega.com>'
        msg.preamble = 'Multipart message.\n'

        part = MIMEText(
            'Estimado {},\n\n'
            'Adjunta le enviamos la factura {}-{}.\n '
            'Para cualquier duda, contacte con nosotros.\n\n'
            'Un saludo,\n\n'
            'FAVEGA S.L.\n'
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
            logger.error("Error sending email to", invoice['customer_email'], e)
        else:
            logger.info("Successfully sent email to", invoice['customer_email'])


def create_output_dir():
    try:
        os.mkdir(OUTPUT_DIR)
    except OSError as e:
        if e.errno == errno.EEXIST:
            logger.info('Could not create output directory: directory already exists.')
        else:
            logger.error('Could not create output directory:', e)


def create_no_email_output_dir():
    try:
        os.mkdir(NO_EMAIL_OUTPUT_DIR)
    except OSError as e:
        if e.errno == errno.EEXIST:
            logger.info('Could not create output directory: directory already exists.')
        else:
            logger.error('Could not create output directory:', e)


if __name__ == "__main__":
    create_output_dir()
    create_no_email_output_dir()
    with open('invoices.txt', 'r') as file:
        parser = InvoiceParser()
        invoices = parser.parse_invoices("".join(file.readlines()))
        invoices_with_no_email = [invoice for invoice in invoices if not invoice['customer_email']]
        invoices_with_email = [invoice for invoice in invoices if invoice['customer_email']]
        for invoice in invoices:
            rendered_latex = InvoiceRenderer().render_invoice(invoice)
            if invoice.get('customer_email'):
                pdf_file = os.path.join(OUTPUT_DIR, "Factura {}-{}.pdf".format(invoice['series'], invoice['number']))
            else:
                pdf_file = os.path.join(NO_EMAIL_OUTPUT_DIR, "Factura {}-{}.pdf".format(invoice['series'],
                                                                                        invoice['number']))
            LatexToPdfConverter.export(rendered_latex, pdf_file)
            if invoice.get('customer_email'):
                InvoiceEmailer.send_invoice(invoice, pdf_file)

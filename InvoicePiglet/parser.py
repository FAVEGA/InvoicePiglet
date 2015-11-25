# coding=utf-8
import logging
import re

from InvoicePiglet.settings import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def parse_products(invoice_string):
    products = []
    for match in re.findall(PRODUCT_REGEX, invoice_string):
        product = {
            'description': match[0].strip(),
            'amount': match[1].strip(),
            'price': match[2].strip(),
            'discount': match[3].strip(),
            'discounted_price': match[4].strip()
        }
        products.append(product)
    return products


def parse_single_invoice(invoice_string):
    invoice = {}
    for (field, regex) in INVOICE_REGEXES:
        invoice[field] = re.search(regex, invoice_string).group(1).strip()
    invoice['products'] = parse_products(invoice_string)
    return invoice


def parse_invoices(input_string):
    invoice_strings = [s for s in input_string.split('<DOC.INI>') if s]
    invoices = []
    for invoice in invoice_strings:
        invoices.append(parse_single_invoice(invoice))
    return invoices

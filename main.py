from InvoicePiglet.invoice_emailer import email_invoice
from InvoicePiglet.invoice_renderer import render_invoice, export_latex_to_pdf
from InvoicePiglet.parser import parse_invoices
from InvoicePiglet.settings import *

if __name__ == "__main__":
    with open('invoices.txt', 'r') as file:
        invoices = parse_invoices("".join(file.readlines()))
    for invoice in invoices:
        rendered_latex = render_invoice(invoice)
        if invoice.get('customer_email'):
            pdf_file = os.path.join(OUTPUT_DIR, "Factura {}-{}.pdf".format(invoice['series'], invoice['number']))
        else:
            pdf_file = os.path.join(NO_EMAIL_OUTPUT_DIR, "Factura {}-{}.pdf".format(invoice['series'],
                                                                                    invoice['number']))
        export_latex_to_pdf(rendered_latex, pdf_file)
        if invoice.get('customer_email'):
            email_invoice(invoice, pdf_file)
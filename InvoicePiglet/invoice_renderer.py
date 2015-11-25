import copy
import logging
import re
import subprocess

import errno
from jinja2 import Environment, FileSystemLoader

from InvoicePiglet.settings import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def render_invoice(invoice):
    logger.debug(invoice)
    invoice = escape_dict_values_latex(invoice)
    logger.debug(invoice)
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
    template = env.get_template('invoice.tex.j2')
    return template.render(invoice)


def escape_dict_values_latex(invoice):
    invoice = copy.deepcopy(invoice)
    for k, v in invoice.items():
        if type(v) == str:
            invoice[k] = escape_latex(v)
        elif type(v) == dict:
            invoice[k] = escape_dict_values_latex(v)
    return invoice


def export_latex_to_pdf(latex, pdf_file_location):
    temp_file = pdf_file_location.replace('.pdf', '.tex')

    try:
        os.mkdir(os.path.dirname(pdf_file_location))
    except OSError as e:
        if e.errno != errno.EEXIST:
            logger.error('Could not create output directory:', e)

    with open(temp_file, 'w', encoding='utf-8') as tf:
        tf.write(latex)

    command = ['pdflatex', temp_file, '-enable-installer', '-output-directory',
               os.path.dirname(pdf_file_location)]
    logger.info("Executing " + " ".join(command))

    FNULL = open(os.devnull, 'w')
    subprocess.call(command, shell=True, stdout=FNULL, stderr=FNULL)
    os.remove(temp_file)
    os.remove(temp_file.replace('.tex', '.aux'))
    os.remove(temp_file.replace('.tex', '.log'))


def get_sanitized_regex_group(self, regex, string):
    return self.escape_latex(re.search(regex, string).group(1).strip())


def split_input_string(input_string):
    return [s for s in input_string.split('<DOC.INI>') if s]


def escape_latex(string):
    for (character, escape) in LATEX_ESCAPES:
        string = string.replace(character, escape)
    return string

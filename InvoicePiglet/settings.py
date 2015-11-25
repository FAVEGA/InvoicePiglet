import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'out')
NO_EMAIL_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'no_email_output')

LATEX_ESCAPES = [
    ('\\', '\\textbackslash{}'),
    ('{', '\\{'),
    ('}', '\\}'),
    ('^', '\\^{}'),
    ('~', '\\~{}'),
    ('&', '\\&'),
    ('_', '\\_'),
    ('#', '\\#'),
    ('$', '\\$'),
    ('%', '\\%'),
]

PRODUCT_REGEX = ("<producto>(?P<description>.*)</>"
                 "(?P<amount>.*)</>"
                 "(?P<price>.*)</>"
                 "(?P<discount>.*)</>"
                 "(?P<discounted_price>.*)")

INVOICE_REGEXES = [
    ('bank_info', "<cobro_ccc_banco>(.*)"),
    ('series', '<factura_serie>(.*)'),
    ('number', '<factura_numero>(.*)'),
    ('date', '<factura_fecha>(.*)'),
    ('gross_total', '<importe_producto>(.*)'),
    ('early_payment_discount_percent', '<dto_pronto_pago_porc>(.*)'),
    ('early_payment_discount_amount', '<dto_pronto_pago_importe>(.*)'),
    ('vat_return_percent', '<recargo_equiv_1_tipo>(.*)'),
    ('vat_return_amount', '<recargo_equiv_1_cuota>(.*)'),
    ('net_total', '<total_a_pagar>(.*)'),
    ('payment_method', '<cliente_nombre_forma_cobro>(.*)'),
    ('expiration_date', '<vencimientos_fechas>(.*)'),
    ('expiration_surcharge', '<vencimientos_importes>(.*)'),
    ('tax_1_taxable_amount', '<impuesto_1_base>(.*)'),
    ('tax_1_percent', '<impuesto_1_tipo>(.*)'),
    ('tax_1_amount', '<impuesto_1_cuota>(.*)'),
    ('tax_2_taxable_amount', '<impuesto_2_base>(.*)'),
    ('tax_2_percent', '<impuesto_2_tipo>(.*)'),
    ('tax_2_amount', '<impuesto_2_cuota>(.*)'),
    ('tax_3_taxable_amount', '<impuesto_3_base>(.*)'),
    ('tax_3_percent', '<impuesto_3_tipo>(.*)'),
    ('tax_3_taxable_amount', '<impuesto_3_cuota>(.*)'),
    ('income_tax_percent', '<retencion_irpf_tipo>(.*)'),
    ('income_tax_amount', '<retencion_irpf_cuota>(.*)'),
    ('customer_code', "<cliente_codigo>(.*)"),
    ('customer_name', "<cliente_tit_lic_fiscal>(.*)"),
    ('customer_country', "<cliente_codigo_pais>(.*)"),
    ('customer_id', "<cliente_nif>(.*)"),
    ('customer_address', "<administracion_via_publica>(.*)"),
    ('customer_city', "<administracion_poblacion>(.*)"),
    ('customer_state', "<administracion_provincia>(.*)"),
    ('customer_zip_code', "<administracion_codigo_postal>(.*)"),
    ('customer_email', "<administracion_email>(.*)"),
]


SMTP_SERVER = ''
SMTP_PORT = ''
SMTP_USER = ''
SMTP_PASSWORD = ''

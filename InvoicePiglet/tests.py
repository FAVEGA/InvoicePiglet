from .invoice_renderer import escape_dict_values_latex


def test_escape_dict_latex():
    d = {'products': [
        {'description': '%', },
    ]}
    escaped = escape_dict_values_latex(d)
    assert escaped['products'][0]['description'] == r'\%'

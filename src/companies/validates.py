import re


def is_valid_cnpj(cnpj):
    # valida os formatos:
    # 00000000000, 00000000000000, 000.000.000-00, 00.000.000/0000-00, 000000000-00 e 00000000/0000-00
    patterns = [
        r'^\d{11}$',  # 00000000000
        r'^\d{14}$',  # 00000000000000
        r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',  # 000.000.000-00
        r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',  # 00.000.000/0000-00
        r'^\d{9}-\d{2}$',  # 000000000-00
        r'^\d{8}/\d{4}-\d{2}$'  # 00000000/0000-00
    ]

    return any(re.match(pattern, cnpj) for pattern in patterns)


def is_valid_cnae(cnae):
    # valida o formato "0000000" "00.00-0-00"
    pattern = r"^\d{2}\.?\d{2}\-?\d{1}\-?\d{2}$"
    return bool(re.match(pattern, cnae))


def is_not_empty(field):
    return True if len(field) > 0 else False

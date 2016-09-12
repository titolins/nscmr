
SHIPPING_CODES = {
    41106: 1,  # PAC
    40010: 2, # SEDEX
}

PAGSEGURO_STATUS = {
    1: 'Aguardando pagamento',
    2: 'Pagamento em análise',
    3: 'Transação paga',
    4: 'Transação paga',
    5: 'Transação em disputa',
    6: 'Transação devolvida',
    7: 'Transação cancelada pelo(a) ',
    8: 'Transação devolvida',
    9: 'Transação retida temporariamente'
}

UNKNOWN_SHIPPING = 3

def get_pagseguro_shipping_code(correios_code):
    return SHIPPING_CODES.get(correios_code, UNKNOWN_SHIPPING)



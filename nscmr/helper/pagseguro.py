
SHIPPING_CODES = {
    41106: 1,  # PAC
    40010: 2, # SEDEX
}

UNKNOWN_SHIPPING = 3

def get_pagseguro_shipping_code(correios_code):
    return SHIPPING_CODES.get(correios_code, UNKNOWN_SHIPPING)



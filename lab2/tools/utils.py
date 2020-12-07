from tools.exceptions import SignatureError

# from exceptions import SignatureError


def gcd(p, q):
    """Returns the greatest common divisor of p and q"""

    while q != 0:
        (p, q) = (q, p % q)
    return p


def extended_gcd(a, b):
    """
    Returns a tuple (r, i, j) such that r = gcd(a, b) = ia + jb
    """
    # r = gcd(a,b) i = multiplicitive inverse of a mod b
    #      or      j = multiplicitive inverse of b mod a

    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a  # Remember original a/b to remove
    ob = b  # negative values from return results
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob 
    if ly < 0:
        ly += oa  
    return a, lx, ly


def validate_data(data, required, field=''):
    if field:
        field += ' '
    try:
        errors = [key for key in required if key not in data.keys()]
    except AttributeError:
        raise SignatureError(payload={f'{field}': 'Not a JSON dictionary'})

    if errors:
        raise SignatureError(payload={f'{field}required fields': ', '.join(required), 'invalid_field': errors})


def hex_dict_to_int(data):
    for key, value in data.items():
        data[key] = int(value, 16)
    return data
import re, os
from unicodedata import normalize
from PIL import Image

from functools import reduce
from operator import mul
from math import ceil, sqrt, pow

# not the ideal solution, setting a fixed maximum size for the box
# considering that we do not want to set standard boxes as of now
MAX_BOX_SIZE = (20, 20, 10) # sizes in centimeters
MAX_BOX_CAP = 0.8

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(str(word, 'utf-8'))
    return delim.join(result)

def make_thumb(image, path, size=(350,480)):
    filename = image.split('.',1)[0]
    ext = image.rsplit('.',1)[1]
    if ext.lower() == 'jpg':
        ext = 'jpeg'
    image = '{}.{}'.format(filename, ext)
    full_img_path = os.path.join(path, image)
    thumb_filename = '{}_{}.{}'.format(filename, 'thumbnail', ext)
    print(thumb_filename)
    output_file = os.path.join(path, thumb_filename)
    try:
        im = Image.open(full_img_path)
        print('ok')
        im.thumbnail(size)
        im.save(output_file, ext)
        print('ok2')
        return thumb_filename
    except IOError as e:
        print('Erro criando thumbnail de {}'.format(image))
        print(e)

def get_cart_info(cart):
    from ..models import Variant, Product

    max_box_vol = reduce(mul, MAX_BOX_SIZE)*MAX_BOX_CAP
    cart_vol = 0
    cart_weight = 0
    cart_val = 0
    for item in cart:
        var = Variant.get_by_id(item['_id'], to_obj=True)
        p = var.product
        p_vol = reduce(mul,
            (d_val for d,d_val in p.shipping.items() if d is not 'weight'))
        cart_vol += p_vol
        cart_weight += p.shipping['weight']
        cart_val += var.price
    n_boxes = ceil(cart_vol/max_box_vol)
    shipping_sizes = list(i for i in map(lambda x:x*n_boxes, MAX_BOX_SIZE))
    shipping_sizes.append(sqrt(
        pow(shipping_sizes[0],2) +
        pow(shipping_sizes[1],2) +
        pow(shipping_sizes[2],2)))

    return shipping_sizes,cart_weight,cart_val



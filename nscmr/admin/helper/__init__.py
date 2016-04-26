import re, os
from unicodedata import normalize
from PIL import Image

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(str(word, 'utf-8'))
    return delim.join(result)

def make_thumb(image, path, size=(128,128)):
    full_img_path = os.path.join(path, image)
    ext = image.rsplit('.',1)[1]
    filename = image.split('.',1)[0]
    thumb_filename = '{}_{}.{}'.format(filename, 'thumbnail', ext)
    output_file = os.path.join(path, thumb_filename)
    try:
        im = Image.open(full_img_path)
        im.thumbnail(size)
        im.save(output_file, ext)
        return thumb_filename
    except IOError as e:
        print('Erro criando thumbnail de {}'.format(image))
        print(e)

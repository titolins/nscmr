import os
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms import TextField
from wtforms.fields import SelectField
from wtforms.widgets import TextInput
from wtforms.validators import input_required, ValidationError

from flask.ext.uploads import UploadSet, IMAGES


EXT_ALLOWED_MSG = ' '.join([
    'Extensão de arquivo não permitida. Por favor,',
    'selecione um arquivo com uma das seguintes extensões:',
    ', '.join(IMAGES)])

category_images = UploadSet(
        'categoryImages',
        IMAGES,
        default_dest=\
            lambda app: os.path.join(app.instance_path,'uploads/img/category'))


class NsInput(TextInput):
    def __init__(self, ns_class='form-control'):
        super().__init__()
        self.form_class = ns_class

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = '{} {}'.format(self.form_class, c)
        return super().__call__(field, **kwargs)

class NewCategoryForm(Form):
    name = TextField('Nome',
            validators=[input_required("Campo necessário!")],
            widget=NsInput())
    parent = SelectField('Categoria pai')
    base_img = FileField('Base image',
            validators=[
                FileRequired("Campo necessário!"),
                FileAllowed(category_images, message=EXT_ALLOWED_MSG)])
    meta_description = TextField('Meta-description', widget=NsInput())
    '''
    header = FileField('Imagem de cabeçalho',
            validators=[
                FileRequired("Campo necessário!"),
                FileAllowed(category_images, message=EXT_ALLOWED_MSG)])
    '''



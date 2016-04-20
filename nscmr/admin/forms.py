import os
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms.fields import (
    StringField,
    SelectField,
    BooleanField,
    FieldList,
    FormField)

from wtforms.fields.html5 import DecimalField, IntegerField

from wtforms.widgets import TextInput, html5
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

product_images = UploadSet(
        'productImages',
        IMAGES,
        default_dest=\
            lambda app: os.path.join(app.instance_path,'uploads/img/product'))


class NsTextInput(TextInput):
    def __init__(self, ns_class='form-control'):
        super().__init__()
        self.form_class = ns_class

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = '{} {}'.format(self.form_class, c)
        return super().__call__(field, **kwargs)


class NsNumberInput(html5.NumberInput):
    def __init__(self, ns_class='form-control', step=None):
        super().__init__()
        self.form_class = ns_class
        self.step = step

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = '{} {}'.format(self.form_class, c)
        return super().__call__(field, **kwargs)


class NewCategoryForm(Form):
    name = StringField('Nome',
            validators=[input_required("Campo necessário!")],
            widget=NsTextInput())
    parent = SelectField('Categoria pai')
    base_img = FileField('Base image',
            validators=[
                FileRequired("Campo necessário!"),
                FileAllowed(category_images, message=EXT_ALLOWED_MSG)])
    meta_description = StringField('Meta-description', widget=NsTextInput())


class VariantForm(Form):
    color = StringField('Cor', widget=NsTextInput())
    size = StringField('Tamanho', widget=NsTextInput())
    price = DecimalField('Preço',
        validators=[input_required("Campo necessário!")],
        widget=NsNumberInput(step='0.01'))
    quantity = IntegerField('Quantidade',
        validators=[input_required("Campo necessário!")],
        widget=NsNumberInput(step='1'))
    sku = StringField('SKU',
        validators=[input_required("Campo necessário!")],
        widget=NsTextInput())
    images = FieldList(
        FileField('Imagem',validators=[
            FileRequired("Campo necessário!"),
            FileAllowed(product_images, message=EXT_ALLOWED_MSG)]),
        min_entries=4)


class NewProductForm(Form):
    name = StringField('Nome',
        validators=[input_required("Campo necessário!")],
        widget=NsTextInput())
    description = StringField('Descrição',
        validators=[input_required("Campo necessário!")],
        widget=NsTextInput())
    category = SelectField('Categoria',
        validators=[input_required("Campo necessário!")])
    has_variants = BooleanField(
        'Esse item possui variações de cor e/ou tamanho?')
    variants = FieldList(FormField(VariantForm), min_entries=1)
    sku = StringField('SKU',
        validators=[input_required("Campo necessário!")],
        widget=NsTextInput())
    price = DecimalField('Preço',
        validators=[input_required("Campo necessário!")],
        widget=NsNumberInput(step='0.01'))
    quantity = IntegerField('Quantidade',
        validators=[input_required("Campo necessário!")],
        widget=NsNumberInput(step='1'))
    images = FieldList(
        FileField('Imagem',validators=[
            FileRequired("Campo necessário!"),
            FileAllowed(product_images, message=EXT_ALLOWED_MSG)]),
        min_entries=1)
    meta_description = StringField('Meta-description', widget=NsTextInput())



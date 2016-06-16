import os
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms.fields import (
    StringField,
    PasswordField,
    SelectField,
    BooleanField,
    FieldList,
    FormField)

from wtforms.fields.html5 import DecimalField, IntegerField, DateField

from wtforms.widgets import TextInput, PasswordInput, html5, TextArea, Select
from wtforms.validators import (
    input_required,
    ValidationError,
    Optional,
    Email,
    Regexp)

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

VALID_VARIATIONS = [ 'cor', 'tamanho' ]

class NsTextInput(TextInput):
    def __init__(self, ns_class='form-control'):
        super().__init__()
        self.form_class = ns_class

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = '{} {}'.format(self.form_class, c)
        return super().__call__(field, **kwargs)


class NsSelectInput(Select):
    def __init__(self, ns_class='form-control'):
        super().__init__()
        self.form_class = ns_class

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = '{} {}'.format(self.form_class, c)
        return super().__call__(field, **kwargs)


class NsTextAreaInput(TextArea):
    def __init__(self, ns_class='form-control'):
        super().__init__()
        self.form_class = ns_class

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = '{} {}'.format(self.form_class, c)
        return super().__call__(field, **kwargs)


class NsPasswordInput(PasswordInput):
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


class NsDateInput(html5.DateInput):
    def __init__(self, ns_class='form-control', step=None):
        super().__init__()
        self.form_class = ns_class
        self.step = step

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = '{} {}'.format(self.form_class, c)
        return super().__call__(field, **kwargs)



class VarAttrSelectFieldWidget():
    '''
    should set default settings for the select widget, such as 100% width and
    placeholder stuff..
    '''
    pass


class VarAttrSelectField(SelectField):
    def __init__(
            self, label='', validators=None, remove_duplicates=True, **kwargs):
        super().__init__(label, validators, **kwargs)
        self.choices = [ (var, var.capitalize()) for var in VALID_VARIATIONS ]


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
    attr_1_name = VarAttrSelectField('Variação')
    attr_1_value = StringField('Valor', widget=NsTextInput())
    attr_2_name = VarAttrSelectField('Variação')
    attr_2_value = StringField('Valor', widget=NsTextInput())
    price = DecimalField('Preço',
        validators=[Optional()],
        widget=NsNumberInput(step='0.01'))
    quantity = IntegerField('Quantidade',
        validators=[Optional()],
        widget=NsNumberInput(step='1'))
    sku = StringField('SKU',
        widget=NsTextInput())
    images = FieldList(
        FileField('Imagem',validators=[
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
        widget=NsTextInput())
    price = DecimalField('Preço',
        validators=[Optional()],
        widget=NsNumberInput(step='0.01'))
    quantity = IntegerField('Quantidade',
        validators=[Optional()],
        widget=NsNumberInput(step='1'))
    images = FieldList(
        FileField('Imagem',validators=[
            FileAllowed(product_images, message=EXT_ALLOWED_MSG)]),
        min_entries=1)
    meta_description = StringField('Meta-description', widget=NsTextInput())

    def validate(self):
        rv = super().validate()
        default_fields_errors = False
        if not rv:
            default_fields_errors = True
        if self.has_variants.data:
            for var in self.variants:
                if var.attr_1_name.data not in VALID_VARIATIONS:
                    var.attr_1_name.errors = ['Tipo de variação inválida']
                if var.attr_2_name.data not in VALID_VARIATIONS:
                    var.attr_2_name.errors = ['Tipo de variação inválida']
                if var.attr_1_value.data in ('', None) and \
                        var.attr_2_value.data in ('', None):
                    error_str = 'Ao menos um valor de variação deve ser dado'
                    var.attr_1_value.errors = [error_str]
                    var.attr_2_value.errors = [error_str]
                try:
                    price = float(var.price.data)
                    if price <= 0:
                        raise Exception
                except:
                    var.price.errors = ['Valor de preço inválido']
                try:
                    qty = int(var.quantity.data)
                    if qty <= 0:
                        raise Exception
                except:
                    var.quantity.errors = ['Valor de quantidade inválido']
                if var.sku.data in ('', None):
                    var.sku.errors = ['Campo de sku necessário!']
                n_img = len(var.images)
                n_empty = 0
                img_error = False
                for img in var.images:
                    if img.data.filename in ('', None):
                        n_empty += 1
                if n_empty == n_img:
                    img_error = True
                    var.images.errors = [
                        'O produto precisa ter pelo menos uma imagem']
                if var.attr_1_name.errors or var.attr_1_value.errors or \
                        var.attr_2_name.errors or var.attr_2_value.errors or \
                        var.price.errors or var.quantity.errors or \
                        var.sku.errors or img_error or default_fields_errors:
                    return False
                return True
        if self.sku.data in ('', None):
            self.sku.errors = ['Campo necessário!']
        try:
            price = float(self.price.data)
            if price < 0:
                raise Exception
        except:
            self.price.errors = ['Valor inválido']
        try:
            qty = int(self.quantity.data)
            if qty < 0:
                raise Exception
        except:
            self.quantity.errors = ['Valor inválido']
        n_img = len(self.images)
        n_empty = 0
        img_error = False
        for img in self.images:
            if img.data.filename in ('', None):
                n_empty += 1
        if n_empty == n_img:
            img_error = True
            self.images.errors = [
                'O produto precisa ter pelo menos uma imagem']
        if self.sku.errors or self.price.errors or self.quantity.errors or \
                img_error or default_fields_errors:
            return False
        return True


class AddressForm(Form):
    street_address_1 = StringField('Endereço',
        widget=NsTextInput(),
        validators=[input_required("Campo 'endereço' necessário!")])
    street_address_2 = StringField('Complemento', widget=NsTextInput())
    neighbourhood = StringField('Bairro', widget=NsTextInput())
    city = StringField('Cidade',
        widget=NsTextInput(),
        validators=[input_required("Campo 'cidade' necessário!")])
    zip_code = StringField('Cep',
        widget=NsTextInput(),
        validators=[
            input_required("Campo 'cep' necessário!"),
            Regexp(r'[0-9]{5}-[0-9]{3}',
                message="O cep deve ter o seguinte formato: 12345-678")
        ])
    state = StringField('Estado',
        widget=NsTextInput(),
        validators=[input_required("Campo necessário!")])
    # not needed for now..
    #country
    #phone??


class NewUserForm(Form):
    name = StringField('Nome',
        validators=[input_required("Campo necessário!")],
        widget=NsTextInput())
    dob = DateField("Data de nascimento", validators=[Optional()],
        widget=NsDateInput())
    is_admin = BooleanField(
        'Esse usuário é um administrador do sistema?')
    email = StringField('Email',
        validators=[
            input_required("Campo necessário!"),
            Email('Formato inválido')],
        widget=NsTextInput())
    password = PasswordField('Senha',
        widget=NsPasswordInput(),
        validators=[input_required("Campo necessário!")])
    #addresses = FieldList(FormField(AddressForm), min_entries=1)

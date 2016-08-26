from flask_wtf import Form

from wtforms.fields import (
    StringField,
    PasswordField,
    BooleanField,
    FormField,
    SelectField,
    HiddenField,
    IntegerField
)

from wtforms.fields.html5 import DateField

from wtforms.validators import (
    input_required,
    email,
    equal_to,
    Optional,
    Regexp,
    length)

from .admin.forms import (
    NsTextInput,
    NsPasswordInput,
    NsDateInput,
    NsNumberInput,
    NsTextAreaInput,
    NsSelectInput)

MIN_PASS_LEN = 6
MONTHS = [ (i, i) for i in range(13) ]
CREDIT_CARD_BRAND_CHOICES = [
    ('visa', 'Visa'),
    ('master', 'MasterCard'),
]

class LoginForm(Form):
    email = StringField(
        'Email',
        validators=[
            input_required("Campo necessário!"),
            email("Email inválido!")],
            widget=NsTextInput())

    password = PasswordField(
            'Senha',
            [input_required("Campo necessário!")],
            widget=NsPasswordInput())


class ProfileForm(Form):
    name = StringField('Nome', validators=[input_required("Campo necessário!")])
    email = StringField(
        'Email',
        validators=[
            input_required("Campo necessário!"),
            email("Email inválido!")])
    dob = DateField(
            "Data de nascimento",
            validators=[Optional()])
    password = PasswordField(
            'Senha',
            validators=[
                input_required("Campo necessário!"),
                equal_to('confirm', message="As senhas precisam ser iguais")])
    confirm = PasswordField(
            'Confirme sua senha', [input_required("Campo necessário!")])


class AddressForm(Form):
    street_address_1 = StringField('Endereço', widget=NsTextInput())
    street_number = IntegerField('Número', widget=NsNumberInput())
    street_address_2 = StringField('Complemento', widget=NsTextInput())
    neighbourhood = StringField('Bairro', widget=NsTextInput())
    city = StringField('Cidade', widget=NsTextInput())
    zip_code = StringField('Cep', widget=NsTextInput())
    state = StringField('Estado', widget=NsTextInput())
    # not needed for now..
    #country
    #phone??


class RegistrationForm(Form):
    name = StringField(
        'Nome',
        validators=[input_required("Campo necessário!")],
        widget=NsTextInput())
    email = StringField(
        'Email',
        validators=[
            input_required("Campo necessário!"),
            email("Email inválido!")],
        widget=NsTextInput())
    dob = DateField(
        "Data de nascimento",
        validators=[Optional()],
        widget=NsDateInput())
    password = PasswordField(
        'Senha',
        validators=[
            input_required("Campo necessário!"),
            length(
                min=MIN_PASS_LEN,
                message="A senha deve conter ao menos {} caractéres.".\
                    format(MIN_PASS_LEN)),
            equal_to('confirm', message="As senhas precisam ser iguais")],
        widget=NsPasswordInput())
    confirm = PasswordField(
        'Confirme sua senha', [input_required("Campo necessário!")],
        widget=NsPasswordInput())
    has_address = BooleanField('Gostaria de cadastrar algum endereço?')
    address = FormField(AddressForm)
    # address and phone as custom fields, perhaps...

    def validate(self):
        rv = super().validate()
        default_fields_errors = False
        address_fields_errors = False
        if not rv:
            default_field_errors = True
        if self.has_address.data:
            address_data = self.address.data
            for field,value in address_data.items():
                if field != 'street_address_2' and value in (None, 'None', ''):
                    getattr(self.address, field).errors = ['Campo necessário!']
                    address_fields_errors = True
                if field == 'zip_code':
                    field = getattr(self.address, field)
                    validator = Regexp(r'[0-9]{5}-[0-9]{3}',
                        message="Formato inválido")
                    try:
                        validator(self.address, field)
                    except:
                        field.errors.append(validator.message)
                        address_fields_errors = True
            if default_fields_errors or address_fields_errors:
                return False
        return True


class ContactForm(Form):
    name = StringField(
        'Nome',
        validators=[input_required("Campo necessário!")],
        widget=NsTextInput())
    email = StringField(
        'Email',
        validators=[
            input_required("Campo necessário!"),
            email("Email inválido!")],
            widget=NsTextInput())
    subject = StringField(
        'Assunto',
        validators=[input_required("Campo necessário!")],
        widget=NsTextInput())
    message = StringField(
        'Mensagem',
        validators=[input_required("Campo necessário!")],
        widget=NsTextAreaInput())


class CustomMadeForm(Form):
    name = StringField(
        'Nome',
        validators=[input_required("Campo necessário!")],
        widget=NsTextInput())
    email = StringField(
        'Email',
        validators=[
            input_required("Campo necessário!"),
            email("Email inválido!")],
            widget=NsTextInput())
    product_type = StringField(
        'Tipo de produto',
        validators=[input_required("Campo necessário!")],
        widget=NsTextInput())
    sizes = StringField(
        'Medidas',
        validators=[input_required("Campo necessário!")],
        widget=NsTextInput())
    message = StringField(
        'Conte um pouco mais sobre suas ideias!',
        validators=[input_required("Campo necessário!")],
        widget=NsTextAreaInput())

class CreditCardForm(Form):
    holder_name = StringField('Nome do titular',
        validators=[input_required("Campo necessário!")],
        widget=NsTextInput())
    number = StringField('Número',
        validators=[input_required("Campo necessário!")],
        widget=NsTextInput())
    brand = HiddenField('Bandeira',
        validators=[input_required("Campo necessário")])
    security_code = StringField('Número de segurança',
        validators=[input_required("Campo necessário!")],
        widget=NsTextInput())
    exp_month = SelectField('Mês',
        choices=MONTHS,
        validators=[input_required("Campo necessário!")],
        widget=NsSelectInput())
    exp_year = IntegerField('Ano',
        validators=[input_required("Campo necessário!")],
        widget=NsNumberInput(step='1'))


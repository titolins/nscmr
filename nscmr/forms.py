from flask.ext.wtf import Form

from wtforms import (
    TextField,
    PasswordField,
    SubmitField,
    ValidationError,
    FieldList,
    FormField
)

from wtforms.fields.html5 import DateField

from wtforms.validators import (
    input_required,
    email,
    equal_to,
    Optional,
    Regexp)

class LoginForm(Form):
    email = TextField(
        'Email',
        validators=[
            input_required("Campo necessário!"),
            email("Email inválido!")])

    password = PasswordField('Senha', [input_required("Campo necessário!")])


class ProfileForm(Form):
    name = TextField('Nome', validators=[input_required("Campo necessário!")])
    email = TextField(
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
    name = TextField('Nome', validators=[input_required("Campo necessário!")])
    street_address_1 = TextField('Nome',
        validators=[input_required("Campo necessário!")])
    street_address_2 = TextField('Complemento')
    city = TextField('Cidade',validators=[input_required("Campo necessário!")])
    zip_code = TextField('Cep',
        validators=[
            input_required("Campo necessário!"),
            Regexp(r'[0-9]{5}-[0-9]{3}', message="Formato inválido")
        ])
    state = TextField('Estado', [input_required("Campo necessário!")])
    # not needed for now..
    #country
    #phone??


class RegistrationForm(Form):
    name = TextField('Nome', validators=[input_required("Campo necessário!")])
    email = TextField(
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
    # address and phone as custom fields, perhaps...

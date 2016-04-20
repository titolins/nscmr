from flask_wtf import Form

from wtforms.fields import (
    StringField,
    PasswordField,
)

from wtforms.fields.html5 import DateField

from wtforms.validators import (
    input_required,
    email,
    equal_to,
    Optional,
    Regexp,
    length)

MIN_PASS_LEN = 6

class LoginForm(Form):
    email = StringField(
        'Email',
        validators=[
            input_required("Campo necessário!"),
            email("Email inválido!")])

    password = PasswordField('Senha', [input_required("Campo necessário!")])


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
    name = StringField('Nome', validators=[input_required("Campo necessário!")])
    street_address_1 = StringField('Nome',
        validators=[input_required("Campo necessário!")])
    street_address_2 = StringField('Complemento')
    city = StringField('Cidade',validators=[input_required("Campo necessário!")])
    zip_code = StringField('Cep',
        validators=[
            input_required("Campo necessário!"),
            Regexp(r'[0-9]{5}-[0-9]{3}', message="Formato inválido")
        ])
    state = StringField('Estado', [input_required("Campo necessário!")])
    # not needed for now..
    #country
    #phone??


class RegistrationForm(Form):
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
                length(
                    min=MIN_PASS_LEN,
                    message="A senha deve conter ao menos {} caractéres.".\
                        format(MIN_PASS_LEN)),
                equal_to('confirm', message="As senhas precisam ser iguais")])
    confirm = PasswordField(
            'Confirme sua senha', [input_required("Campo necessário!")])
    # address and phone as custom fields, perhaps...

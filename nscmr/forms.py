from flask.ext.wtf import Form
from nscmr.admin.forms import RedirectForm

from wtforms import (
    TextField,
    PasswordField,
    SubmitField,
    ValidationError
)

from wtforms.fields.html5 import DateField

from wtforms.validators import input_required, email, equal_to, Optional

class LoginForm(RedirectForm):
    email = TextField(
        'email',
        validators=[
            input_required("Campo necessário!"),
            email("Email inválido!")])

    password = PasswordField('senha', [input_required("Campo necessário!")])


class RegistrationForm(RedirectForm):
    name = TextField('nome', validators=[input_required("Campo necessário!")])
    email = TextField(
        'email',
        validators=[
            input_required("Campo necessário!"),
            email("Email inválido!")])
    dob = DateField(
            "data de nascimento",
            format='%d/%m/%Y',
            validators=[Optional()])
    password = PasswordField(
            'senha',
            validators=[
                input_required("Campo necessário!"),
                equal_to('confirm', message="As senhas precisam ser iguais")])
    confirm = PasswordField(
            'confirme sua senha', [input_required("Campo necessário!")])

from flask.ext.wtf import Form
from nscmr.admin.forms import RedirectForm

from wtforms import (
    TextField,
    PasswordField,
    SubmitField,
    ValidationError,
    DateField
)

from wtforms.validators import input_required, email

class LoginForm(RedirectForm):
    email = TextField(
        'email',
        validators=[
            input_required("Campo necessário!"),
            email("Email inválido!")])

    password = PasswordField('senha', [input_required("Campo necessário!")])


class RegistrationForm(RedirectForm):
    name = TextField('name', validators=[input_required("Campo necessário!")])
    email = TextField(
        'email',
        validators=[
            input_required("Campo necessário!"),
            email("Email inválido!")])
    dob = DateField(format='%d/%m/%Y')
    password = PasswordField('senha',[input_required("Campo necessário!")])
    confirm_password = PasswordField(
            'senha',[input_required("Campo necessário!")])

import sendgrid
from sendgrid.helpers.mail import *

from flask import current_app as app, render_template

TEXT_EMAIL_CONTENT = '''
        Prezado(a) {}\n,
        Sua compra n. {} foi concluída com sucesso.\n
        Agradecemos por nos escolher! Para acompanhar o seu andamento, entre
        na sua conta no site do StudioDuvet e acesse seu perfil clicando no
        link com seu nome na barra superior.\n
        Agradecemos novamente pela preferência!\n
        Um grande abraço,\n
        Studio Duvet
    '''


def send_confirmation_mail(user, order):
    sg = sendgrid.SendGridAPIClient(apikey=app.config.get('SENDGRID_API_KEY'))
    from_email = Email(
        email=app.config.get('SUPPORT_CONTACT'),
        name='Studio Duvet')
    subject = "StudioDuvet | Sua compra"
    to_email = Email(
        email=user.email,
        name=user.name)

    text_content = Content(
        type="text/plain",
        value=TEXT_EMAIL_CONTENT.format(
            user['name'].capitalize(),
            order['reference']))

    html_content= Content(
        type="text/html",
        value=render_template(
            'confirmationemail.html', user=user, order=order))

    mail = Mail(
        from_email=from_email,
        subject=subject,
        to_email=to_email,
        content=text_content)
    mail.add_content(html_content)

    print(mail.get())

    r = sg.client.mail.send.post(request_body=mail.get())
    print(r.status_code)
    print(r.body)
    print(r.headers)



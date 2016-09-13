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

STATUS_CHANGE_EMAIL_CONTENT = '''
    Você recebeu uma notificação de mudança de status do pagseguro.\n\n
    A seguinte mudança foi notificada:\n\n
    Ordem de compra n. {}\n
    Comprador: {}\n
    Mensagem: {}\n
    Código: {}\n\n
    Dados de entrega:\n
    \tEndereço:\n
    \t{}, {} {} - {}\n
    \t{} - {}\n\n
    \tEntrega:\n
    \tTipo: {}\n
    \tValor: {}\n\n
    Att.,\n
    Studio Duvet
    '''

def send_status_change_email(order, change_data):
    order = order.__dict__['_content']
    from_email = Email(
        email=app.config.get('SUPPORT_CONTACT'),
        name='Studio Duvet')
    subject = "StudioDuvet | Notificação de Mudança"
    to_email = Email(
        email=user.email,
        name=user.name)
    text_content = Content(
        type="text/plain",
        value=STATUS_CHANGE_EMAIL_CONTENT.format(
            order['reference'],
            order['user']['name'],
            change_data['msg'],
            change_data['code'],
            order['address']['street_address_1'],
            order['address']['street_address_number'],
            order['address']['street_address_2'],
            order['address']['city'],
            order['address']['zip_code'],
            order['address']['state'],
            order['cart']['shipping']['type'],
            "{:.2f}".format(
                order['cart']['shipping']['cost']).replace('.',','),
    ))
    mail = Mail(
        from_email=from_email,
        subject=subject,
        to_email=to_email,
        content=text_content)

    send_email(mail)

def send_confirmation_email(user, order):
    order = order.__dict__['_content']
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
            user.name.capitalize(),
            order['reference']))

    html_content= Content(
        type="text/html",
        value=render_template(
            'confirmationemail.html', user=user, order=order))

    mail = Mail(
        from_email=from_email,
        subject=subject,
        to_email=to_email,
        content=html_content)
    #mail.add_content(html_content)

    duvet_mail = Mail(
        from_email=from_email,
        subject="StudioDuvet | Compra realizada",
        to_email=from_email,
        content=html_content)
    #mail.add_content(html_content)

    print(mail.get())

    send_email(mail)
    send_email(duvet_mail)

def send_email(mail):
    try:
        sg = sendgrid.SendGridAPIClient(apikey=app.config.get('SENDGRID_API_KEY'))
        r = sg.client.mail.send.post(request_body=mail.get())
        print(r.status_code)
        print(r.body)
        print(r.headers)
    except Exception as e:
        print(e.read())
        print(e)


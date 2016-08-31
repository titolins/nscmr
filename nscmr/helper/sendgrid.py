import sendgrid
from sendgrid.helpers.mail import *

from flask import current_app as app

def send_confirmation_mail(user, order):
    sg = sendgrid.SendGridAPIClient(apikey=app.config.get('SENDGRID_API_KEY'))
    from_email = Email(
        email=app.config.get('SUPPORT_CONTACT'),
        name='Studio Duvet')
    subject = "StudioDuvet | Sua compra"
    to_email = Email(
        email=user.email,
        name=user.name)
    text, html = build_confirmation_mail_content(user.name, order.reference)
    text_content = Content(
        type="text/plain",
        value=text)
    html_content= Content(
        type="text/html",
        value=html)

    mail = Mail(
        from_email=from_email,
        subject=subject,
        to_email=to_email,
        content=text_content)
    mail.add_content(html_content)

    print(mail.get())

    r = sg.client.mail.send.post(request_body=mail.get())


def build_confirmation_mail_content(name, order_reference):
    domain = "http://45.55.162.155"
    logo = "{}/static/imgs/logo_studio.png".format(domain)
    def build_html():
        return \
            '''
                <html>
                    <body>
                        <table>
                            <tbody>
                                <tr>
                                    <td>
                                        <img src="{}">
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding-top: 20px">
                                        <h3 style="font-weight: lighter;
                                            text-transform: uppercase;">
                                                parabéns pela sua compra!
                                        </h3>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Prezado Sr(a). {},</td>
                                </tr>
                                <tr>
                                    <td>
                                        <p>
                                            Sua compra n. <b>{}</b> foi
                                            concluída com sucesso.<br>
                                            Para acompanhar o seu andamento,
                                            volte para o site do <a href="{}">
                                            StudioDuvet</a> e entre na sua
                                            conta.<br>
                                            Uma vez logado, acesse o seu perfil
                                            clicando no link com o seu nome na
                                            barra superior e selecionando
                                            perfil no menu.<br>
                                            Ao selecionar suas compras, você
                                            poderá confirmar os produtos
                                            adquiridos, assim como o endereço
                                            de entrega e o seu andamento.<br>
                                        </p>
                                        <p>
                                            Agradecemos novamente pela
                                            preferência!<br>
                                            Um grande abraço,
                                            Studio Duvet
                                        </p>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </body>
                </html>
            '''.format(
                logo,
                name,
                order_reference,
                domain
            )
    def build_text():
        return \
            '''
            PARABÉNS PELA SUA COMPRA!\n
            Prezado Sr(a). {},\n
            Sua compra n. {} foi concluída com sucesso.\n
            Para acompanhar o seu andamento, volte para o site do StudioDuvet\n
            e entre na sua conta.
            Uma vez logado, acesse o seu perfil clicando no link com o seu \n
            nome na barra superior e selecionando perfil no menu.\n
            Ao selecionar suas compras, você poderá confirmar os produtos \n
            adquiridos, assim como o endereço de entrega e o seu andamento.\n

            Agradecemos novamente pela preferência!\n
            Um grande abraço,\n
            Studio Duvet
            '''.format(
                name,
                order_reference,
            )
    return (build_html(), build_text())


#! /usr/bin/python

from email.mime.text import MIMEText
from smtplib import SMTP
from validate_email import validate_email  # requiere pyDNS

from credenciales import usuario, clave


def verificarCorreo(correo):
    return validate_email(correo, verify=True)


def enviarNotificacion(tramite, html):
    if not verificarCorreo(tramite['mail']):
        return

    msg = MIMEText(html, 'html')
    msg['From'] = usuario
    msg['To'] = tramite['mail']
    msg['Subject'] = "[seguidor-siet] %s: %s" % (tramite['desc'],
                                                 tramite['estado'])

    # open up a line with the server
    mailServer = SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.login(usuario, clave)
    mailServer.sendmail(usuario, tramite['mail'], msg.as_string())
    mailServer.close()

import re

from django.contrib import messages
from django.contrib.messages import constants

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def password_is_valid(req, password, confirm_password):
    if len(password) < 6:
        messages.add_message(req, constants.WARNING, "Senha deve conter no mínimo 6 caracteres")
        return False
    
    if not password == confirm_password:
        messages.add_message(req, constants.WARNING, "Senhas digitadas devem ser iguais")
        return False
    
    if not re.search('[A-Z]', password):
        messages.add_message(req, constants.WARNING, "Senha precisa ter no mínimo uma letra maiúscula")
        return False
        
    if not re.search('[a-z]', password):
        messages.add_message(req, constants.WARNING, "Senha precisa ter no mínimo uma letra minúscula")
        return False
        
    if not re.search('[0-9]', password):
        messages.add_message(req, constants.WARNING, "Senha precisa ter no mínimo um número")
        return False
        
    return True



def validate_empty_fields(nome, email, senha, confirma_senha):
    if not nome: return True
    if not email: return True
    if not senha: return True
    if not confirma_senha: return True
    return False



def send_email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)
    email.attach_alternative(html_content,'text/html')
    email.send()
    return {'status': 1}




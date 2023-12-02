from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import password_is_valid, validate_empty_fields, send_email_html
from django.contrib import messages, auth
from django.contrib.messages import constants
from django.contrib.auth.models import User
import os
import json
from django.conf import settings
from .models import Ativacao
from hashlib import sha256
from django.shortcuts import get_object_or_404

# Create your views here.
def cadastro(req):
    if req.user.is_authenticated:
        return redirect('/')
    if req.method == 'GET':
        return render(req, 'cadastro.html',context={})
    if req.method == 'POST':
        usuario=req.POST.get('usuario')
        email=req.POST.get('email')
        senha=req.POST.get('senha')
        confirmar_senha=req.POST.get('confirmar_senha')
        
        has_empty_fields = validate_empty_fields(usuario, email, senha, confirmar_senha)
        if has_empty_fields:
            messages.add_message(req, constants.WARNING, 'Necessário preencher todos os campos')
            return redirect('/auth/cadastro/')
        
        is_valid = password_is_valid(req, senha, confirmar_senha)        
        if not is_valid:
            return redirect('/auth/cadastro/')
        
        userAlreadyExists = User.objects.filter(username=usuario)
        if len(userAlreadyExists) > 0:
            messages.add_message(req, constants.WARNING, 'Usuário já existe')
            return redirect('/auth/cadastro/')
        
        emailAlreadyExists = User.objects.filter(email=email)
        if len(emailAlreadyExists) > 0:
            messages.add_message(req, constants.WARNING, 'Usuário já existe')
            return redirect('/auth/cadastro/')
        
        
        try:
            user = User.objects.create_user(username=usuario, email=email, password=senha, is_active=False)
            user.save()
            
            token=sha256(f'{user.username}{user.email}'.encode()).hexdigest()
            ativacao = Ativacao(token=token, user=user)
            ativacao.save()
            
            path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/emails/cadastro_confirmado.html')
            link=settings.EMAIL_BASE+f'/auth/ativar_conta/{token}'
            print(">>>link", link)
            result= send_email_html(path_template, 'Cadastro confirmado', [email,], username=usuario, link_ativacao=link)
            print(">>>result",result)
            messages.add_message(req, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
            return redirect('/auth/login')
        except:
            messages.add_message(req, constants.ERROR, 'Erro interno do sistema')
            return redirect('/auth/cadastro')

def login(req):
    if req.user.is_authenticated:
        return redirect('/pacientes')
    if req.method == 'GET':
        return render(req, 'login.html',context={})
    if req.method == 'POST':
        try:
            usuario = req.POST.get('usuario')
            senha = req.POST.get('senha')
            user = auth.authenticate(req,username=usuario, password=senha)
            
            if not user:
                messages.add_message(req, constants.WARNING, 'Nome ou senha inválidos')
                return redirect('/auth/login')
            
            if not user.is_active:
                messages.add_message(req, constants.WARNING, 'Usuário ainda não ativado')
                return redirect('/auth/login')
            
            auth.login(req, user)
            return redirect('/pacientes')
        except:
            messages.add_message(req, constants.ERROR, 'Something went wrong')    
            return redirect('/auth/login')

def logout(req):
    auth.logout(req)
    return redirect('/auth/login')


def ativar_conta(req, token):
    try:
        token = get_object_or_404(Ativacao, token=token)
        
        if token.ativo:
            messages.add_message(req, constants.ERROR, 'Token inválido!')
            return redirect('/auth/login')
        
        user = User.objects.get(username=token.user.username, email=token.user.email)
        if not user:
            messages.add_message(req, constants.ERROR, 'Usuário inválido!')
            return redirect('/auth/login')

        user.is_active = True
        user.save()
        token.ativo = True
        token.save()
        messages.add_message(req, constants.SUCCESS, 'Conta ativada com sucesso!')
        return redirect('/auth/login')
    except:
        messages.add_message(req, constants.ERROR, 'Erro ativando conta')
        return redirect('/auth/login')


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Paciente, DadosPaciente, Refeicao, Opcao
from django.shortcuts import redirect
from .util import email_ja_existe, idade_valida, tem_campo_vazio
from django.contrib import messages
from django.contrib.messages import add_message, constants
from datetime import datetime
from django.http import JsonResponse


@login_required(login_url='/auth/login/')
def paciente(req):
    if req.method=='GET':
        pacientes = Paciente.objects.filter(nutri=req.user)
        return render(req, 'pacientes.html', context={'pacientes':pacientes})
    if req.method=='POST':
        nome = req.POST.get('nome')
        sexo = req.POST.get('sexo')
        idade = req.POST.get('idade')
        email = req.POST.get('email')
        telefone = req.POST.get('telefone')
        
        if tem_campo_vazio(nome=nome, sexo=sexo, idade=idade, email=email, telefone=telefone):
            messages.add_message(req, constants.WARNING, 'Todos os campos devem ser preenchidos')
            return redirect('/pacientes')
        
        if not idade_valida(idade):
            messages.add_message(req, constants.WARNING, 'Idade deve ser numérico')
            return redirect('/pacientes')
        
        if email_ja_existe(email):
            messages.add_message(req, constants.WARNING, 'Email já existe')
            return redirect('/pacientes')
        
        try:
            nutri = req.user
            paciente = Paciente(nome=nome, sexo=sexo, idade=idade, email=email, telefone=telefone, nutri=nutri)
            paciente.save()
            messages.add_message(req, constants.SUCCESS, 'Paciente cadastrado com sucesso')
            return redirect('/pacientes')
        except:
            messages.add_message(req, constants.ERROR, 'Erro interno do sistema')
            return redirect('/pacientes')
        
    

@login_required(login_url='/auth/login/')
def dados_pacientes_listar(req):
    if req.method == 'GET':
        try:
            pacientes = Paciente.objects.filter(nutri = req.user)
            return render(req, 'dados_pacientes_listar.html', context={'pacientes':pacientes})
        except Exception as e:
            messages.add_message(req, constants.ERROR, f'Something went wrong - {e}')
            return render(req, 'dados_pacientes_listar.html', context={'pacientes':pacientes})


# def getKey(self):
#     print(self, self.data)
#     return self.data


@login_required(login_url='/auth/login/')
def dados_paciente(req, id):
    if req.method == 'GET':
        try:
            paciente = Paciente.objects.get(id=id, nutri=req.user)
            dados = DadosPaciente.objects.filter(paciente=paciente)
            dados=sorted(dados, key=lambda x: x.data, reverse=True)
            return render(req, 'dados_paciente.html', context={'paciente':paciente, 'dados':dados})
        except Exception as e:
            messages.add_message(req, constants.ERROR, f'Something went wrong - {e}')
            pacientes = Paciente.objects.filter(nutri = req.user)
            return render(req, 'dados_pacientes_listar.html', context={'pacientes':pacientes})
    if req.method == 'POST':
        try:
            peso = req.POST.get('peso')    
            altura = req.POST.get('altura')    
            gordura = req.POST.get('gordura')    
            musculo = req.POST.get('musculo')    
            hdl = req.POST.get('hdl')    
            ldl = req.POST.get('ldl')    
            colesterol_total = req.POST.get('ctotal')    
            trigliceridios = req.POST.get('trigliceridios')    
            user_id = req.POST.get('user_id')
        
            if  len(peso.strip()) == 0 or \
                len(altura.strip()) == 0 or \
                len(gordura.strip()) == 0 or \
                len(musculo.strip()) == 0 or \
                len(hdl.strip()) == 0 or \
                len(ldl.strip()) == 0 or \
                len(colesterol_total.strip()) == 0 or \
                len(trigliceridios.strip()) == 0:
                messages.add_message(req, constants.WARNING, 'Todos os campos devem ser preenchidos')
                return redirect(f'/dados_paciente/{user_id}')
            
            user=Paciente.objects.get(id=user_id, nutri=req.user)
            
            dados = DadosPaciente(
                data=datetime.now(), 
                peso=peso, 
                altura=altura, 
                percentual_gordura=gordura, 
                percentual_musculo=musculo, 
                colesterol_hdl=hdl, 
                colesterol_ldl=ldl, 
                colesterol_total=colesterol_total, 
                trigliceridios=trigliceridios, 
                paciente=user
            )
            dados.save()
            messages.add_message(req, constants.SUCCESS, 'Dados salvos com sucesso')
            return redirect(f'/dados_paciente/{user_id}')
        except Exception as e:    
            messages.add_message(req, constants.ERROR, f'Something went wrong - {e}')
            return redirect(f'/dados_paciente/{user_id}')
        
    

from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/auth/login')
@csrf_exempt
def grafico_peso(req, id):
    paciente = Paciente.objects.get(id=id)
    dados=DadosPaciente.objects.filter(paciente=paciente).order_by('data')
    
    pesos = [dado.peso for dado in dados]
    labels = list(range(len(pesos)))
    print('>>>', labels)
    data = {
        'pesos': pesos,
        'labels': labels,
    }
    # return render(req, 'dados_paciente.html', context={"data":data})
    return JsonResponse(data)
    
    
@login_required(login_url='/auth/login/')
def plano_alimentar_listar(req):
    if req.method == 'GET':
        try:
            pacientes = Paciente.objects.filter(nutri=req.user)
            return render(req, 'plano_alimentar_listar.html', context={'pacientes':pacientes})
        except Exception as e:
            messages.add_message(req, constants.ERROR, f'Something went wrong - {e}')
            return redirect('/auth/login')
    



@login_required(login_url='/auth/login/')
def plano_alimentar(req, id):
    if req.method == 'GET':
        try:
            paciente = Paciente.objects.get(id=id, nutri=req.user)
            refeicoes = Refeicao.objects.filter(paciente=paciente).order_by('horario')
            opcoes = Opcao.objects.filter(refeicao__in=refeicoes)
            return render(req, 'plano_alimentar.html', context={'paciente':paciente, 'refeicoes': refeicoes, 'opcoes': opcoes})
        except Exception as e:
            messages.add_message(req, constants.ERROR, f'Something went wrong - {e}')
            return redirect('/plano_alimentar_listar/')





@login_required(login_url='/auth/login/')
def refeicao(req, id_paciente):
    if req.method == 'POST':
        try:
            titulo = req.POST.get('titulo')
            horario = req.POST.get('horario')
            carboidratos = req.POST.get('carboidratos')
            proteinas = req.POST.get('proteinas')
            gorduras = req.POST.get('gorduras')
            paciente = Paciente.objects.get(id=id_paciente, nutri=req.user)
            
            r1 = Refeicao(
                titulo=titulo,
                horario=horario,
                carboidratos=carboidratos,
                proteinas=proteinas,
                gorduras=gorduras,
                paciente=paciente
            )
            r1.save()
            messages.add_message(req, constants.SUCCESS, 'Refeição cadastrada com sucesso')
            return redirect(f'/plano_alimentar/{id_paciente}')
            
        except Exception as e:
            messages.add_message(req, constants.ERROR, f'Something went wrong - {e}')
            return redirect(f'/plano_alimentar/{id_paciente}')



@login_required(login_url='/auth/login/')
def opcao(req, id_paciente):
    if req.method == 'POST':
        try:
            imagem = req.FILES.get('imagem')
            descricao = req.POST.get('descricao')
            id_refeicao = req.POST.get('refeicaoo')
            paciente = Paciente.objects.get(id=id_paciente)
            refeicao = Refeicao.objects.get(id=id_refeicao)
            op1 = Opcao(imagem=imagem, descricao=descricao, refeicao=refeicao)
            op1.save()
            messages.add_message(req, constants.SUCCESS, 'Opção cadastrada com sucesso')
            return redirect(f'/plano_alimentar/{paciente.id}')
        except Exception as e:
            messages.add_message(req, constants.ERROR, f'Something went wrong - {e}')
            return redirect(f'/plano_alimentar/{paciente.id}')


import pdfkit
from django.template.loader import render_to_string
from django.conf import settings

@login_required(login_url='/auth/login')
def pdf(req, id):
    try:
        paciente = Paciente.objects.get(id=id, nutri=req.user)
        refeicoes = Refeicao.objects.filter(paciente=paciente).order_by('horario')
        opcoes = Opcao.objects.filter(refeicao__in=refeicoes)

        teste = render_to_string(request=req, template_name='plano_alimentar.html', context={'paciente':paciente, 'refeicoes': refeicoes, 'opcoes': opcoes})
        teste = teste.replace('src="/media/', f'src="{settings.MEDIA_ROOT}/')
        teste = teste.replace('src="/static/plataforma/',f'src="{settings.STATICFILES_DIRS[0]}/plataforma/')

        path_wkhtmltopdf = settings.ENV('path_wkhtmltopdf')
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        path_to_save_pdf = settings.ENV('path_to_save_pdf')+f'/pdf_user_{paciente.id}.pdf'
        
        pdfkit.from_string(teste, path_to_save_pdf , configuration=config, options = {'enable-local-file-access': True})

        messages.add_message(req, constants.SUCCESS, 'PDF gerado com sucesso')
        return redirect(f'/plano_alimentar/{paciente.id}')
    except Exception as e:
        messages.add_message(req, constants.ERROR, f'Something went wrong - {e}')
        return redirect(f'/plano_alimentar/{paciente.id}')
    






    
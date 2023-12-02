from .models import Paciente

def tem_campo_vazio(nome, sexo, idade, email, telefone):
    try:
        if not nome.strip() or not sexo.strip() or not idade.strip() or not email.strip() or not telefone.strip():
            return True
        return False
    except:
        return True


def idade_valida(idade):
    try:
        if idade.isnumeric():
            return True
        return False
    except:
        return False



def email_ja_existe(email):
    try:
        foundPaciente=Paciente.objects.filter(email=email)
        if len(foundPaciente) > 0:
            return True
        return False
    except:
        return False

    
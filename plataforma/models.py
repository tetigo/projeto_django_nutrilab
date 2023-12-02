from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Paciente(models.Model):
    choices_sexo=(
        ('F', 'feminino'),
        ('M', 'masculino'),
    )
    nome = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, choices=choices_sexo)
    idade = models.IntegerField()
    email = models.EmailField()
    telefone = models.CharField(max_length=19)
    nutri = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.nome




class DadosPaciente(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data = models.DateTimeField()
    peso = models.IntegerField()
    altura = models.IntegerField()
    percentual_gordura = models.IntegerField()
    percentual_musculo = models.IntegerField()
    colesterol_hdl = models.IntegerField()
    colesterol_ldl = models.IntegerField()
    colesterol_total = models.IntegerField()
    trigliceridios = models.IntegerField()
    
    def __str__(self) -> str:
        return f'{self.paciente.nome}, {self.peso} kg'
    
    

class Refeicao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50)
    horario = models.TimeField()
    carboidratos = models.IntegerField()
    proteinas = models.IntegerField()
    gorduras = models.IntegerField()
    
    def __str__(self) -> str:
        return self.titulo
    
    
    
class Opcao(models.Model):
    refeicao = models.ForeignKey(Refeicao, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='opcao')
    descricao = models.TextField()
    
    def __str__(self) -> str:
        return self.descricao
    
    
    


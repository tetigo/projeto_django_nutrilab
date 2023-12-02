from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ativacao(models.Model):
    class Meta:
        verbose_name='ativacao'
        verbose_name_plural = 'ativacoes'
    token = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ativo = models.BooleanField(default=False) # indica se este token ja foi utilizado
    
    def __str__(self):
        return self.user.username
    
    

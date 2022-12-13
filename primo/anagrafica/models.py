import os
from datetime import datetime

import PyPDF2
from django.core.exceptions import ValidationError
from django.db import models
from PyPDF2 import PdfReader


# Create your models here.



class Persona(models.Model):
    nome = models.CharField(max_length=50,blank=True, null=True)
    cognome = models.CharField(max_length=50,blank=True, null=True)
    indirizzo = models.CharField(max_length=50,blank=True, null=False,verbose_name="indirizzo di residenza",help_text="inserisci qui l'indirizzo dove abita la persona")
    data_di_nascita = models.DateField()

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Persone"
        unique_together = [['nome', 'cognome']]

    def __str__(self):
        return str(self.nome) + " " + str(self.cognome)

    def nome_cognome(self):
        return str(self.nome) + " " + str(self.cognome)
        #return str(self.nome).capitalize() + " " + str(self.cognome).capitalize()

    def clean(self):
        if not self.data_di_nascita:
            raise ValidationError({"data_di_nascita":"Inserire la data di nascita"})
        elif self.data_di_nascita > datetime.now().date():
            raise ValidationError({"data_di_nascita":"La data di nascita deve essere precedente ad oggi"})
        #TODO: Implementare un controllo sulla lunghezza del nome che deve essere > di 2
        if (len(self.nome)) <= 2 :
            raise ValidationError ({"nome" : " Il nome deve essere almeno di 3 caratteri"})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.nome = str(self.nome).capitalize()
        self.cognome = str(self.cognome).capitalize()
        super(Persona, self).save()




class Studente (Persona):
    voto = models.SmallIntegerField(verbose_name='voto medio',default=0)
    def clean (self):
        super(Studente, self).clean()
        if self.voto >30 or self.voto<0:
            raise ValidationError({"voto": "Voto non valido, deve essere massimo 30"})
    class Meta:
        verbose_name = "Studente"
        verbose_name_plural = "Studenti"





class Materia(models.Model):
    nome_materia = models.CharField(max_length=30, blank = False)
    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materie"
    def __str__(self):
        return str(self.nome_materia)

class Compito (models.Model):
    tipo_compito = models.ForeignKey(Materia,max_length=15, blank = False, on_delete=models.CASCADE)
    studente = models.ForeignKey(Studente, blank = False, null = False, on_delete = models.CASCADE)
    voto = models.PositiveSmallIntegerField()
    allegato = models.FileField(upload_to='file',blank=True,null=True)

    def clean(self):
        if self.voto > 30:
            raise ValidationError({"voto": "Voto non valido, deve essere massimo 30"})

    class Meta:
        verbose_name = "Compito"
        verbose_name_plural = "Compiti"

    def __str__(self):
        return str(self.tipo_compito) + " " + str(self.studente)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        comps = Compito.objects.filter(studente=self.studente)
        totale = 0
        studente = self.studente
        for compito in comps :
            totale+= compito.voto
        media=totale/len(comps)
        studente.voto=media
        studente.save()
        super(Compito,self).save()

class Professore(Persona):
    materia = models.ForeignKey(Materia,max_length=15, blank = False, on_delete=models.CASCADE)
    voto = models.ForeignKey(Compito,max_length=15, blank = False, on_delete=models.CASCADE)




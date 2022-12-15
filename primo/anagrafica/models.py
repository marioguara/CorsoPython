import email
import os
import smtplib
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename
from xml.dom import ValidationErr

from django.core.exceptions import ValidationError
from django.db import models
from django.core.mail import send_mail


# Create your models here.


class Persona(models.Model):
    nome = models.CharField(max_length=50, blank=True, null=True)
    cognome = models.CharField(max_length=50, blank=True, null=True)
    indirizzo = models.CharField(max_length=50, blank=True, null=False, verbose_name="indirizzo di residenza",
                                 help_text="inserisci qui l'indirizzo dove abita la persona")
    data_di_nascita = models.DateField()

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Persone"
        unique_together = [['nome', 'cognome']]

    def __str__(self):
        return str(self.nome) + " " + str(self.cognome)

    def nome_cognome(self):
        return str(self.nome) + " " + str(self.cognome)
        # return str(self.nome).capitalize() + " " + str(self.cognome).capitalize()

    def clean(self):
        if not self.data_di_nascita:
            raise ValidationError({"data_di_nascita": "Inserire la data di nascita"})
        elif self.data_di_nascita > datetime.now().date():
            raise ValidationErr or({"data_di_nascita": "La data di nascita deve essere precedente ad oggi"})
        # TODO: Implementare un controllo sulla lunghezza del nome che deve essere > di 2
        if (len(self.nome)) <= 2:
            raise ValidationError({"nome": " Il nome deve essere almeno di 3 caratteri"})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.nome = str(self.nome).capitalize()
        self.cognome = str(self.cognome).capitalize()
        super(Persona, self).save()


class Studente(Persona):
    voto = models.SmallIntegerField(verbose_name='voto medio', default=0)

    def clean(self):
        super(Studente, self).clean()
        if self.voto > 30 or self.voto < 0:
            raise ValidationError({"voto": "Voto non valido, deve essere massimo 30"})

    class Meta:
        verbose_name = "Studente"
        verbose_name_plural = "Studenti"



class Materia(models.Model):
    nome_materia = models.CharField(max_length=30, blank=False)

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materie"

    def __str__(self):
        return str(self.nome_materia)


class Compito(models.Model):
    tipo_compito = models.ForeignKey(Materia, max_length=15, blank=False, on_delete=models.CASCADE)
    studente = models.ForeignKey(Studente, blank=False, null=False, on_delete=models.CASCADE)
    voto = models.PositiveSmallIntegerField()
    allegato = models.FileField(upload_to='file', blank=True, null=True)

    def sendmail(self):
        msg = MIMEText(f"IL VOTO DEL COMPITO E: {self.voto} <br> LA MEDIA DI TUTTI I VOTI E: {self.studente.voto}",'html')
        genitori = Genitore.objects.filter(figlio=self.studente)
        destinatari = []
        for genitore in genitori:
            destinatari.append(genitore.email)
        msg['Subject'] = f"ESITO COMPITO DI {self.tipo_compito} dell'alunno {self.studente}"
        msg['To'] = ", ".join(destinatari)
        msg['From'] = 'service.signalling@mermec.com'
        msg['Date'] = formatdate(localtime=True)
        s = smtplib.SMTP_SSL('smtps.aruba.it:465')
        s.login('service.signalling@mermec.com', 'SerVice!2019')
        msg = MIMEMultipart()
        msg.attach(MIMEImage(self.allegato("download.pdf").read()))
        s.sendmail(from_addr='service.signalling@mermec.com', to_addrs=destinatari, msg=msg.as_string())
        s.quit()


    def clean(self):
        if self.voto > 30:
            raise ValidationError({"voto": "Voto non valido, deve essere massimo 30"})

    class Meta:
        verbose_name = "Compito"
        verbose_name_plural = "Compiti"

    def __str__(self):
        return str(self.tipo_compito) + " " + str(self.studente)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        totale = 0
        studente = self.studente
        super(Compito, self).save()
        comps = Compito.objects.filter(studente=self.studente)

        for compito in comps:
            totale += compito.voto
            if len(comps) == 0 or totale == 0:
                media = 0
            else:
                media = totale / len(comps)
        studente.voto = media
        studente.save()
        self.sendmail()

class Professore(Persona):
    materia = models.ForeignKey(Materia, max_length=15, blank=False, on_delete=models.CASCADE)
    voto = models.ForeignKey(Compito, max_length=15, blank=False, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Professore"
        verbose_name_plural = "Professori"

class Genitore(Persona):
    figlio = models.ForeignKey(Studente, blank=False, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, blank=True, null=True, unique=True)
    class Meta:
        verbose_name = "Genitore"
        verbose_name_plural = "Genitori"

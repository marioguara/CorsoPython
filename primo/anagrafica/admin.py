from django.contrib import admin
from django.core.mail import send_mail

from anagrafica.models import Persona, Studente , Compito, Materia, Genitore, Professore


class PersonaAdmin(admin.ModelAdmin):
    list_display = ["nome_cognome","indirizzo","data_di_nascita"]
    fieldsets = (
        ('Dati persona', {'fields': (('nome',"cognome"), "data_di_nascita")}),
        ('Indirizzo', {'fields': ('indirizzo', )}),
    )
admin.site.register(Persona, PersonaAdmin)



class StudenteAdmin(PersonaAdmin):
    fieldsets = (
        ('Dati persona', {'fields': (('nome', "cognome", "data_di_nascita"),)}),
        ('Indirizzo', {'fields': ('indirizzo',)}),
        ('Dati compito', {'fields': ('voto',)})
    )
    readonly_fields = ["voto",]


admin.site.register(Studente, StudenteAdmin)

class CompitoAdmin(admin.ModelAdmin):
    fields = ['studente', 'tipo_compito','voto','allegato',]


admin.site.register(Compito, CompitoAdmin)

admin.site.register(Materia)
class GenitoreAdmin(PersonaAdmin):
    fieldsets = (
        ('Dati persona', {'fields': (('nome', "cognome"), "data_di_nascita")}),
        ('Dati figlio', {'fields': ('figlio',)}),
        ('Dati email', {'fields': ('email',)}),
    )
admin.site.register(Genitore, GenitoreAdmin)
class ProfessoreAdmin(PersonaAdmin):
    fieldsets = (
        ('Dati persona', {'fields': (('nome', "cognome"), "data_di_nascita")}),
        ('Indirizzo', {'fields': ('indirizzo',)}),
        ('Materia insegnante', {'fields': ('materia',)}),
        ('Media voti classe', {'fields': ('voto',)}),
    )
admin.site.register(Professore, ProfessoreAdmin)

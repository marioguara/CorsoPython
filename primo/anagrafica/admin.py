from django.contrib import admin

from anagrafica.models import Persona, Studente , Compito, Materia


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
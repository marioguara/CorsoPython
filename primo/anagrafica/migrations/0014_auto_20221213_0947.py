# Generated by Django 3.2.16 on 2022-12-13 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0013_alter_studente_voto'),
    ]

    operations = [
        migrations.AddField(
            model_name='compito',
            name='allegato',
            field=models.FileField(blank=True, null=True, upload_to='file'),
        ),
        migrations.CreateModel(
            name='Professore',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='anagrafica.persona')),
                ('materia', models.ForeignKey(max_length=15, on_delete=django.db.models.deletion.CASCADE, to='anagrafica.materia')),
                ('voto', models.ForeignKey(max_length=15, on_delete=django.db.models.deletion.CASCADE, to='anagrafica.compito')),
            ],
            bases=('anagrafica.persona',),
        ),
    ]
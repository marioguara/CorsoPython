# Generated by Django 3.2.16 on 2022-12-12 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anagrafica', '0006_alter_persona_data_di_nascita'),
    ]

    operations = [
        migrations.CreateModel(
            name='Studente',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='anagrafica.persona')),
            ],
            bases=('anagrafica.persona',),
        ),
    ]

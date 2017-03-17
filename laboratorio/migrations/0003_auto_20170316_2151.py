# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 02:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio', '0002_auto_20170316_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='codigo',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='unidadMedida',
            field=models.CharField(choices=[('mg', 'Miligramos'), ('g', 'Gramos'), ('kg', 'Kilogramos'), ('ml', 'Mililitros'), ('l', 'Litros'), ('unknown', 'unknown')], default='unknown', max_length=10),
        ),
        migrations.AlterField(
            model_name='bodega',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 16, 21, 51, 33, 932000)),
        ),
        migrations.AlterField(
            model_name='producto',
            name='clasificacion',
            field=models.CharField(choices=[('Materiales Vivos', (('Bac', 'Bacterias'), ('Hon', 'Hongos'))), ('Medios de Cultivo', (('Glu', 'Glucosa'), ('Fru', 'Fructuosa'), ('Tri', 'Triptona'), ('Pep', 'Peptona'))), ('Micronutrientes', (('Fe', 'Hierro'), ('Mg', 'Magnesio'), ('P', 'Fosforo'))), ('Manipulacion ADN y Proteinas', (('Pri', 'Primers'), ('Kem', 'Kits de extraccion metagenomica'), ('KeADN', 'Kits de extraccion ADN aislado'), ('Pup', 'Purificador de proteinas'), ('Enr', 'Enzimas de restriccion'), ('Pro', 'Proteasas'))), ('Otros', 'Moleculas genericas')], max_length=35),
        ),
        migrations.AlterField(
            model_name='producto',
            name='valorUnitario',
            field=models.DecimalField(decimal_places=4, max_digits=7),
        ),
    ]

# Generated by Django 3.1.6 on 2021-04-21 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselSlider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200, unique=True)),
                ('real', models.CharField(blank=True, default='', max_length=200)),
                ('acteurs', models.CharField(blank=True, default='', max_length=200)),
                ('genre', models.CharField(blank=True, default='', max_length=200)),
                ('annee', models.SmallIntegerField(blank=True, null=True)),
                ('duree', models.SmallIntegerField(blank=True, null=True)),
                ('pays', models.CharField(default='', max_length=200)),
                ('age', models.SmallIntegerField(blank=True, null=True)),
                ('synopsis', models.TextField(blank=True, default='', max_length=10000)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('page_allocine', models.URLField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Seance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('lieu', models.CharField(blank=True, default='', max_length=200)),
                ('animations', models.TextField(blank=True, default='', max_length=10000)),
                ('plein_air', models.BooleanField(default=False)),
                ('festival', models.BooleanField(default=False)),
                ('mois_du_doc', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Projection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heure', models.TimeField()),
                ('animation', models.TextField(blank=True, default='', max_length=10000)),
                ('tarif', models.SmallIntegerField(blank=True, null=True)),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seances.film')),
                ('seance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seances.seance')),
            ],
        ),
    ]

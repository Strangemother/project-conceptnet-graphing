# Generated by Django 2.2.3 on 2019-07-28 01:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0007_auto_20190728_0055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plural', models.CharField(blank=True, max_length=255, null=True)),
                ('plural_noun', models.CharField(blank=True, max_length=255, null=True)),
                ('plural_verb', models.CharField(blank=True, max_length=255, null=True)),
                ('plural_adj', models.CharField(blank=True, max_length=255, null=True)),
                ('singular_noun', models.CharField(blank=True, max_length=255, null=True)),
                ('present_participle', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='tokenword',
            name='tense',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first.Tense'),
        ),
    ]
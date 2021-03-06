# Generated by Django 2.2.3 on 2019-07-27 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0002_temporalinput_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(help_text='Word', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TokenWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(help_text='Word', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='first.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='PositionTokenWord',
            fields=[
                ('tokenword_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='first.TokenWord')),
                ('position', models.SmallIntegerField()),
            ],
            bases=('first.tokenword',),
        ),
        migrations.AddField(
            model_name='temporalinput',
            name='tokens',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='first.PositionTokenWord'),
        ),
    ]

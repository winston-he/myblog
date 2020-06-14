# Generated by Django 3.0.3 on 2020-04-11 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('blog', '0002_auto_20200309_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to='user.User'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(help_text='Please fill it in!', max_length=140),
        ),
        migrations.AlterField(
            model_name='comment',
            name='disliked_by',
            field=models.ManyToManyField(related_name='disliked_comments', to='user.User'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_comments', to='user.User'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='user.User'),
        ),
        migrations.AlterField(
            model_name='post',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_posts', to='user.User'),
        ),
        migrations.AlterField(
            model_name='post',
            name='marked_by',
            field=models.ManyToManyField(related_name='marked_posts', to='user.User'),
        ),
    ]
# Generated by Django 2.2.6 on 2019-11-20 17:23

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_title', models.CharField(max_length=200, verbose_name='Title of the news')),
                ('news_sh_description', models.CharField(max_length=800, verbose_name='Short description of the news')),
                ('news_content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('news_tag', models.CharField(choices=[('Другое', 'Другое'), ('Казахстанская-премьер лига', 'Казахстанская-премьер лига'), ('Национальная сборная по футболу', 'Национальная сборная по футболу'), ('Лига чемпионов УЕФА', 'Лига чемпионов УЕФА'), ('Лига Европы УЕФА', 'Лига Европы УЕФА')], default='Другое', max_length=100)),
                ('publication_date', models.DateTimeField(verbose_name='Date of publication of the news')),
                ('count_of_views', models.IntegerField(verbose_name='Count of views of the news')),
                ('img', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='UserFavourite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Fav_news_ID', to='news.News')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User_ID', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('avatar', models.ImageField(default='images/avatars/defavatar.jpg', null=True, upload_to='images/avatars/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(verbose_name='Content of comment')),
                ('comment_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date of publication of the comment')),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.News')),
            ],
        ),
    ]

# Generated by Django 2.2.4 on 2019-08-07 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='이메일')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
                ('shipping_address', models.TextField(verbose_name='배송주소')),
                ('is_staff', models.BooleanField(default=False, verbose_name='직원계정')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='관리자계정')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '고객',
                'verbose_name_plural': '고객',
                'db_table': 'customer',
            },
        ),
    ]

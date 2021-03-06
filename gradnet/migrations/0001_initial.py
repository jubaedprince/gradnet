# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-10 03:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Alumni',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_of', models.CharField(choices=[('2010', '2010'), ('2011', '2011'), ('2012', '2012')], max_length=4)),
                ('current_location', models.CharField(max_length=100)),
                ('avatar', models.ImageField(upload_to='alumni/avatar')),
                ('phone', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=100)),
                ('current_position', models.CharField(blank=True, max_length=100)),
                ('current_employer', models.CharField(blank=True, max_length=100)),
                ('short_bio', models.CharField(blank=True, max_length=200)),
                ('alternate_email', models.CharField(blank=True, max_length=200)),
                ('facebook_url', models.CharField(blank=True, max_length=200)),
                ('twitter_url', models.CharField(blank=True, max_length=200)),
                ('other_contact_method', models.CharField(blank=True, max_length=200)),
                ('spare_time_in_a_week', models.CharField(choices=[('<3 hours', '<3 hours'), ('3-6 hours', '3-6 hours'), ('6-10 hours', '6-10 hours'), ('I\u2019m available', 'I\u2019m available'), ('Can\u2019t say ', 'Can\u2019t say ')], max_length=100)),
                ('preferred_payment_method', models.CharField(choices=[('Bank', 'Bank'), ('Paypal', 'Paypal'), ('Venmo', 'Venmo'), ('Bkash', 'Bkash')], max_length=100)),
                ('bank_routing_number', models.CharField(blank=True, max_length=100)),
                ('bank_account_number', models.CharField(blank=True, max_length=100)),
                ('paypal_email', models.CharField(blank=True, max_length=100)),
                ('paypal_phone', models.CharField(blank=True, max_length=100)),
                ('venmo_email', models.CharField(blank=True, max_length=100)),
                ('venmo_phone', models.CharField(blank=True, max_length=100)),
                ('bkash_phone', models.CharField(blank=True, max_length=100)),
                ('preparation_time', models.CharField(choices=[('<1 month', '<1 month'), ('1-3 months', '1-3 months'), ('3-6 months', '3-6 months'), ('>6 months', '>6 months')], max_length=100)),
                ('preparation_type', models.CharField(choices=[('Regular & Rigorous', 'Regular & Rigorous'), ('Fully-employed, mostly weekends', 'Fully-employed, mostly weekends'), ('Mostly weekends, rigorous before the test', 'Mostly weekends, rigorous before the test')], max_length=100)),
                ('preparation_path', models.CharField(blank=True, max_length=200)),
                ('preparation_helpful_books_or_resources', models.CharField(max_length=200)),
                ('preparation_school_selection_path', models.CharField(max_length=200)),
                ('preparation_reason_to_pick_current_school', models.CharField(max_length=200)),
                ('preparation_essay_resume_importance', models.CharField(max_length=200)),
                ('preparation_essay_resume_writing_approach', models.CharField(blank=True, max_length=200)),
                ('preparation_best_experience', models.CharField(blank=True, max_length=200)),
                ('preparation_challenging_part', models.CharField(blank=True, max_length=200)),
                ('preparation_advice', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('aliases', models.CharField(max_length=1000)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=300)),
                ('cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('subscribe_to_newsletter', models.BooleanField(default=True)),
                ('accepts_terms', models.BooleanField(default=True)),
                ('current_occupation', models.CharField(max_length=100)),
                ('graduation_year', models.CharField(max_length=4)),
                ('undergrad_in', models.CharField(max_length=100)),
                ('other_high_school_degrees', models.CharField(max_length=100)),
                ('work_experience_1', models.CharField(max_length=100)),
                ('work_experience_1_from', models.CharField(max_length=4)),
                ('work_experience_1_to', models.CharField(max_length=4)),
                ('work_experience_2', models.CharField(max_length=100)),
                ('work_experience_2_from', models.CharField(max_length=4)),
                ('work_experience_2_to', models.CharField(max_length=4)),
                ('work_experience_3', models.CharField(max_length=100)),
                ('work_experience_3_from', models.CharField(max_length=4)),
                ('work_experience_3_to', models.CharField(max_length=4)),
                ('gmat_score', models.CharField(max_length=100)),
                ('gre_score', models.CharField(max_length=100)),
                ('extra_curricular_activities', models.CharField(max_length=100)),
                ('volunteer_involvements', models.CharField(max_length=100)),
                ('other_activities_or_projects', models.CharField(max_length=100)),
                ('programs_applying_to', models.CharField(max_length=100)),
                ('countries_applying_to', models.CharField(max_length=100)),
                ('target_school_1', models.CharField(max_length=100)),
                ('target_school_2', models.CharField(max_length=100)),
                ('target_school_3', models.CharField(max_length=100)),
                ('possible_enrollment_year', models.CharField(max_length=4)),
                ('phone', models.CharField(max_length=40)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('logo_image', models.ImageField(upload_to='university/logo')),
                ('university_image', models.ImageField(upload_to='university/university')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=100)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gradnet.Country')),
            ],
            options={
                'verbose_name_plural': 'Universities',
            },
        ),
        migrations.AddField(
            model_name='program',
            name='university',
            field=models.ManyToManyField(to='gradnet.University'),
        ),
        migrations.AddField(
            model_name='alumni',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gradnet.Program'),
        ),
        migrations.AddField(
            model_name='alumni',
            name='providing_services',
            field=models.ManyToManyField(to='gradnet.Service'),
        ),
        migrations.AddField(
            model_name='alumni',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gradnet.University'),
        ),
        migrations.AddField(
            model_name='alumni',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

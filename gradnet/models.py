# coding=utf-8
from __future__ import unicode_literals


from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.conf import settings
from django.template.defaultfilters import slugify, register


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def is_alumni(self):
        result = Alumni.objects.filter(user_id=self.id)
        if result.count() > 0:
            return True
        else:
            return False

    def is_student(self):
        result = Student.objects.filter(user_id=self.id)
        if result.count() > 0:
            return True
        else:
            return False


class Country(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, blank=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super(Country, self).save(*args, **kwargs)


class University(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    logo_image = models.ImageField(upload_to='university/logo')
    university_image = models.ImageField(upload_to='university/university')
    slug = models.SlugField(max_length=100, blank=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Universities"

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super(University, self).save(*args, **kwargs)

    @register.simple_tag
    def get_alumni_count(self, program_slug):
        return Alumni.objects.filter(
            university__slug=self, program__slug=program_slug
        ).count()


class Program(models.Model):
    name = models.CharField(max_length=200)
    aliases = models.CharField(max_length=1000)
    university = models.ManyToManyField(University)
    slug = models.SlugField(max_length=100, blank=True, editable=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)
        super(Program, self).save(*args, **kwargs)


class Service(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=300)
    cost = models.FloatField()

    def __unicode__(self):
        return self.title


class Alumni(models.Model):
    CLASS_OF_CHOICES = (
        ('2010', '2010'),
        ('2011', '2011'),
        ('2012', '2012'),
    )

    SPARE_TIME_CHOICES = (
        ('<3 hours', '<3 hours'),
        ('3-6 hours', '3-6 hours'),
        ('6-10 hours', '6-10 hours'),
        ('I’m available', 'I’m available'),
        ('Can’t say ', 'Can’t say ')
    )

    PAYMENT_METHOD_CHOICES = (
        ('Bank', 'Bank'),
        ('Paypal', 'Paypal'),
        ('Venmo', 'Venmo'),
        ('Bkash', 'Bkash'),
    )

    PREPARATION_TIME_CHOICES = (
        ('<1 month', '<1 month'),
        ('1-3 months', '1-3 months'),
        ('3-6 months', '3-6 months'),
        ('>6 months', '>6 months'),
    )

    PREPARATION_TYPE_CHOICES = (
        ('Regular & Rigorous', 'Regular & Rigorous'),
        ('Fully-employed, mostly weekends', 'Fully-employed, mostly weekends'),
        ('Mostly weekends, rigorous before the test', 'Mostly weekends, rigorous before the test'),
    )



    # # basic
    name = models.CharField(max_length=100)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class_of = models.CharField(max_length=4, choices=CLASS_OF_CHOICES)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    current_location = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='alumni/avatar')
    phone = models.CharField(max_length=200)

    # non mandatory fields:
    slug = models.SlugField(max_length=100, blank=True, editable=False)
    current_position = models.CharField(max_length=100, blank=True)
    current_employer = models.CharField(max_length=100, blank=True)
    short_bio = models.CharField(max_length=200, blank=True)
    alternate_email = models.CharField(max_length=200, blank=True)
    facebook_url = models.CharField(max_length=200, blank=True)
    twitter_url = models.CharField(max_length=200, blank=True)
    other_contact_method = models.CharField(max_length=200, blank=True)

    # # service
    providing_services = models.ManyToManyField(Service)
    spare_time_in_a_week = models.CharField(max_length=100, choices=SPARE_TIME_CHOICES)
    preferred_payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)

    bank_routing_number = models.CharField(max_length=100, blank=True)
    bank_account_number = models.CharField(max_length=100, blank=True)
    paypal_email = models.CharField(max_length=100, blank=True)
    paypal_phone = models.CharField(max_length=100, blank=True)
    venmo_email = models.CharField(max_length=100, blank=True)
    venmo_phone = models.CharField(max_length=100, blank=True)
    bkash_phone = models.CharField(max_length=100, blank=True)

    # # preparation
    preparation_time = models.CharField(max_length=100, choices=PREPARATION_TIME_CHOICES)
    preparation_type = models.CharField(max_length=100, choices=PREPARATION_TYPE_CHOICES)
    preparation_path = models.CharField(max_length=200, blank=True)
    preparation_helpful_books_or_resources = models.CharField(max_length=200)
    preparation_school_selection_path = models.CharField(max_length=200)
    preparation_reason_to_pick_current_school = models.CharField(max_length=200)
    preparation_essay_resume_importance = models.CharField(max_length=200)
    preparation_essay_resume_writing_approach = models.CharField(max_length=200, blank=True)
    preparation_best_experience = models.CharField(max_length=200, blank=True)
    preparation_challenging_part = models.CharField(max_length=200, blank=True)
    preparation_advice = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name + '-' + str(self.user.id))
        super(Alumni, self).save(*args, **kwargs)


class Student(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribe_to_newsletter = models.BooleanField(default=True)
    accepts_terms = models.BooleanField(default=True)
    current_occupation = models.CharField(max_length=100)
    graduation_year = models.CharField(max_length=4)
    undergrad_in = models.CharField(max_length=100)
    other_high_school_degrees = models.CharField(max_length=100)
    work_experience_1 = models.CharField(max_length=100)
    work_experience_1_from = models.CharField(max_length=4)
    work_experience_1_to = models.CharField(max_length=4)
    work_experience_2 = models.CharField(max_length=100)
    work_experience_2_from = models.CharField(max_length=4)
    work_experience_2_to = models.CharField(max_length=4)
    work_experience_3 = models.CharField(max_length=100)
    work_experience_3_from = models.CharField(max_length=4)
    work_experience_3_to = models.CharField(max_length=4)
    gmat_score = models.CharField(max_length=100)
    gre_score = models.CharField(max_length=100)
    extra_curricular_activities = models.CharField(max_length=100)
    volunteer_involvements = models.CharField(max_length=100)
    other_activities_or_projects = models.CharField(max_length=100)
    programs_applying_to = models.CharField(max_length=100)
    countries_applying_to = models.CharField(max_length=100)
    target_school_1 = models.CharField(max_length=100)
    target_school_2 = models.CharField(max_length=100)
    target_school_3 = models.CharField(max_length=100)
    possible_enrollment_year = models.CharField(max_length=4)
    phone = models.CharField(max_length=40)


class Message(models.Model):
    body = models.CharField(max_length=800)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipient')
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __unicode__(self):
        return self.body


class Faq(models.Model):
    question = models.CharField(max_length=800)
    answer = models.CharField(max_length=800)
    publish = models.BooleanField(default=False)

    def __unicode__(self):
        return self.question


class ContactRequest(models.Model):
    body = models.CharField(max_length=800)
    email = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.body


class AlumniStory(models.Model):
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=1000)
    summary = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class Video(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=1000)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    @register.simple_tag
    def id_only(self):
        return self.replace("https://www.youtube.com/watch?v=", "")

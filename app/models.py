from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    phone = models.CharField(max_length=15, null=True)

    avatar = models.ImageField(upload_to='app/static/img/avatars/', null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    rh_token = models.CharField(max_length=255, null=True)

    notification_email = models.BooleanField(default=False)
    notification_sms = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Definition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(null=True, blank=True, unique=True)
    definition = models.TextField(null=True, blank=True)


class Financial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available_funds = models.FloatField()
    funds_held_for_orders = models.FloatField()
    portfolio_value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


class NoteTypes(models.Model):
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=255)


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note_type = models.ForeignKey(NoteTypes, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    value = models.TextField(null=True, blank=True)


class SymbolOfficers(models.Model):
    symbol_id = models.IntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    age = models.CharField(max_length=255, blank=True, null=True)
    salary = models.IntegerField(null=True, blank=True)

    exercised_value = models.IntegerField(null=True, blank=True)
    unexercised_value = models.IntegerField(null=True, blank=True)


class SymbolProfile(models.Model):
    symbol_id = models.IntegerField()
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=6, blank=True, null=True)
    phone = models.CharField(max_length=15, null=True)

    website = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    number_of_employees = models.IntegerField(null=True, blank=True)
    officers = models.ManyToManyField(SymbolOfficers, null=True)


class SymbolNews(models.Model):
    symbol_id = models.IntegerField()
    author = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)

    publisher = models.CharField(max_length=255, null=True, blank=True)
    publisher_time = models.IntegerField(null=True, blank=True)
    summary = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=255, null=True, blank=True)  # news / pr / video
    timezone = models.CharField(max_length=255, null=True, blank=True)
    sentiment_analysis = models.IntegerField(null=True, blank=True)


class Symbol(models.Model):
    # https://api.robinhood.com/instruments/09bc1a2d-534d-49d4-add7-e0eb3be8e640/
    symbol = models.CharField(max_length=15, unique=True, db_index=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    sector = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    ipo_year = models.IntegerField(null=True, blank=True)
    market_cap = models.FloatField(null=True, blank=True)
    listed = models.BooleanField(default=True)
    growth_rate = models.FloatField(null=True, blank=True)

    moving_average = models.FloatField(null=True, blank=True)
    average_volume = models.FloatField(null=True, blank=True)

    current_price = models.FloatField(null=True, blank=True)
    last_close = models.FloatField(null=True, blank=True)
    last_open = models.FloatField(null=True, blank=True)

    notes = models.ManyToManyField(Note, null=True)
    news = models.ManyToManyField(SymbolNews, null=True)
    profile = models.ForeignKey(SymbolProfile, null=True)

    def __str__(self):
        return self.symbol


class SymbolHistory(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    open = models.FloatField(null=True, blank=True)
    high = models.FloatField(null=True, blank=True)
    low = models.FloatField(null=True, blank=True)
    close = models.FloatField(null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.symbol.symbol


class Position(models.Model):
    user = models.ForeignKey(User)
    # todo


class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField()


class Article(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    link = models.ForeignKey(Link, on_delete=models.CASCADE)


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    notes = models.ManyToManyField(Note, related_name='tags', blank=True)
    definitions = models.ManyToManyField(Definition, related_name='tags', blank=True)
    positions = models.ManyToManyField(Position, related_name='tags', blank=True)
    links = models.ManyToManyField(Link, related_name='tags', blank=True)

    # Definition.objects.filter(tags__name="your_tag_name")
    # Notes.objects.item_set.all() - returns all tags for the notes

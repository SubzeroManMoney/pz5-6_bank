# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Account(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.CharField(unique=True, max_length=20)
    type = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3)
    client = models.ForeignKey('Client', models.DO_NOTHING)

    class Meta:
        db_table = 'account'


class Card(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.CharField(unique=True, max_length=16)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    account = models.OneToOneField(Account, models.DO_NOTHING)

    class Meta:
        db_table = 'card'


class Client(models.Model):
    id = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=150)
    passport = models.CharField(unique=True, max_length=20)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'client'


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(max_length=20)
    account = models.ForeignKey(Account, models.DO_NOTHING)

    class Meta:
        db_table = 'transaction'

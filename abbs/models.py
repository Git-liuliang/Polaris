# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class UserInfo(AbstractUser):
    """
    用户信息
    """
    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.username

class Inventory(models.Model):
    nid = models.AutoField(primary_key=True)
    app = models.CharField(max_length=64)
    ip_addr = models.CharField(max_length=64)
    ssh_port = models.IntegerField()
    country = models.CharField(max_length=64)

    manager = models.ManyToManyField(
        to="UserInfo",
        through='Inventory2UserInfo',
        through_fields=('machine', 'user'),
    )

class Inventory2UserInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='manager', to="UserInfo", to_field='nid')
    machine = models.ForeignKey(verbose_name='machine', to="Inventory", to_field='nid')

    class Meta:
        unique_together = [
            ('user', 'machine'),
        ]

    # def __str__(self):
    #     v = self.user.nid + "----" + self.machine.ip_addr
    #     return v

class  task_info(models.Model):
    nid = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    task_id = models.CharField(max_length=64)
    task_args = models.CharField(max_length=64)
    task_result = models.CharField(max_length=64)

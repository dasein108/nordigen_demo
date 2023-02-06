import uuid

from django.db import models
from django_enum import EnumField

# Create your models here.


class NordigenConnectManager(models.Manager):
    pass


class UserRequisition(models.Model):
    class RequisitionStatus(models.IntegerChoices):
        IN_PROGRESS = (0,)
        SUCCESS = (1,)
        FAILED = (-1,)

    requisition_id = models.UUIDField(unique=True, blank=True, null=True)
    institution_id = models.CharField(max_length=120)
    name = models.CharField(max_length=120, default="UNKNOWN")
    reference_id = models.UUIDField(unique=True)
    status = EnumField(RequisitionStatus, default=RequisitionStatus.IN_PROGRESS)

    created_at = models.DateTimeField(auto_now_add=True)
    connected_at = models.DateTimeField(null=True, blank=True)

    user_id = models.UUIDField()

    # TODO: ATTACH TO SPECIFIC USER
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = NordigenConnectManager()
    #
    # def _str_(self):
    #     return f'{self.title}{self.completed}'
    #
    # def save(self, *args, **kwargs):
    #     self.completed_at = now_() if self.completed else None
    #     super(TodoItem, self).save(*args, **kwargs)


class UserAccount(models.Model):
    requisition = models.ForeignKey(UserRequisition, on_delete=models.CASCADE)
    account_id = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField


# Create your models here.

class DataFile(models.Model):
    file = models.FileField(blank=True, upload_to="data")

    def __str__(self):
        return self.file.name


# YG - creating a model to store dag related information. This model will be used by meta core to store
# DAG related information and to track current DAG status.
class Workflow(models.Model):
    STATES = (
        ('CREATED', 'Workflow created'),
        ('STARTED', 'Workflow started'),
        ('IN_PROGRESS', 'Workflow in progress'),
        ('COMPLETED', 'Workflow completed'),
        ('ERROR', 'Error in workflow'),
        ('CANCELLED', 'Workflow cancelled'),
    )
    name = models.CharField(max_length=50, null=True, blank=True)
    owner = models.ForeignKey("auth.User")
    template_id = models.CharField(max_length=50, null=True, blank=True)
    current_fragment_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(choices=STATES, max_length=50, blank=True, null=True)
    workflow = models.CharField(max_length=2000, null=True, blank=True)
    info = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id)

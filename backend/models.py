from django.db import models


class WorkersMain(models.Model):
    UserLogin = models.CharField(max_length=255)
    ShortName = models.CharField(max_length=50)
    UserPassword = models.CharField(max_length=50)

    class Meta:
        db_table = 'Workers_Main'

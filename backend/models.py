from django.db import models


class WorkersMain(models.Model):
    UserLogin = models.CharField(max_length=255)
    ShortName = models.CharField(max_length=50)
    UserPassword = models.CharField(max_length=50)
    RoleManager = models.CharField(max_length=2)
    RoleGager = models.CharField(max_length=2)
    RoleSetter = models.CharField(max_length=2)

    class Meta:
        db_table = 'Workers_Main'


class WorkersUserAccess(models.Model):
    user = models.ForeignKey(WorkersMain, on_delete=models.CASCADE, db_column='user')
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    class Meta:
        db_table = 'Workers_UserAccess'


class OrdersMain(models.Model):
    OrderNumber = models.IntegerField(max_length=11)
    OrderDateTime = models.DateTimeField()
    OrderDateMetering = models.DateField()
    OrderStatus = models.IntegerField(max_length=11)
    OrderAmount = models.IntegerField(max_length=255)
    OrderPaid = models.IntegerField(max_length=255)
    OrderManager = models.IntegerField(max_length=11)
    OrderGager = models.IntegerField(max_length=11)
    OrderSetter = models.IntegerField(max_length=11)

    class Meta:
        db_table = 'Orders_Main'

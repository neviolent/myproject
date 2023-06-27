from django.db import models

class BarcodeManager(models.Manager):
    def get_filtered_data(self, filter_params):
        # Выполнение выборки из таблицы barcodes с заданными фильтрами, в нашем случае штрихкод 4607174577206
        queryset = self.filter(barcode__exact='4607174577206')#тестовый запрос

        return queryset

class barcodes(models.Model):
    barcode = models.CharField(max_length=100)
    product_name = models.CharField(max_length=50)
    product_producer = models.CharField(max_length=100)
    product_description = models.CharField(max_length=200)
    objects = BarcodeManager()

class account(models.Model):
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    realname = models.CharField(max_length=255)
    sex = models.CharField(max_length=255, default=0)
    score = models.IntegerField(default=0)
    reg_timestamp = models.DateTimeField()
    last_login_timestamp = models.DateTimeField()
    auth_key = models.CharField(max_length=255, default=0)

class reviews(models.Model):
    reviewer_id = models.IntegerField(default=0)
    product_barcode = models.CharField(max_length=250)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
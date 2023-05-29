from django.db import models

class BarcodeManager(models.Manager):
    def get_filtered_data(self, filter_params):
        # Выполнение выборки из таблицы barcodes с заданными фильтрами, в нашем случае штрихкод 4607174577206
        queryset = self.filter(barcode__exact='4607174577206')#тестовый запрос

        return queryset

class Barcode(models.Model):
    barcode = models.CharField(ax_length=100)
    product_name = models.CharField(max_length=50)
    product_producer = models.CharField(max_length=100)
    product_description = models.CharField(max_length=200)

    objects = BarcodeManager()
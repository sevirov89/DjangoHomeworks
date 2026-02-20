from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.name} - {self.description}'


class Measurement(models.Model):
    sensor_id = models.ForeignKey(Sensor,on_delete=models.CASCADE, related_name='measurements', verbose_name='Датчик')
    temperature = models.DecimalField(decimal_places=2, max_digits=6, verbose_name="Температура")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата и время изменения")

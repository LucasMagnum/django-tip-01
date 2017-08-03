from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_adult = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.id)

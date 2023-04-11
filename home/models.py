from django.db import models

class Database(models.Model):
    cid = models.IntegerField()
    company = models.CharField(max_length = 200)


class DataDetails(models.Model):
    cid = models.IntegerField()
    data = models.TextField()

    def __str__(self):
        return f"{self.data}"

class DataExt(models.Model):
    cid = models.IntegerField()
    data = models.TextField()

    def __str__(self):
        return f"{self.data}"
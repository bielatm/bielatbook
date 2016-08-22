from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateTimeField()
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

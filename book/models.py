from django.db import models


class UserProfile(models.Model):
    user_id = models.OneToOneField('auth.User')
    date_of_birth = models.DateField()
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.user_id.username

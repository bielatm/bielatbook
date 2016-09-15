from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user_id = models.OneToOneField('auth.User')
    date_of_birth = models.DateField()
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.user_id.username


class FriendshipInvite(models.Model):
    user = models.ForeignKey('auth.User', related_name='sent_friendship_invites')
    friend = models.ForeignKey('auth.User', related_name='received_friendship_invites')


class Friendship(models.Model):
    user = models.ForeignKey('auth.User')
    friend = models.ForeignKey('auth.User', related_name='friendships')


class Message(models.Model):
    author = models.ForeignKey('auth.User', related_name='sent_messages')
    text = models.TextField()
    receiver = models.ForeignKey('auth.User', related_name='received_messages')
    created_at = models.DateTimeField(default=timezone.now)


class Group(models.Model):
    admin = models.ForeignKey('auth.User', related_name='user_groups')
    name = models.CharField(max_length=50)
    description = models.TextField()


class Post(models.Model):
    group = models.ForeignKey(Group)
    author = models.ForeignKey('auth.User')
    text = models.TextField()

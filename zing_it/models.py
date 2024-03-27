from django.db import models
import datetime

# Create your models here.


class Playlist(models.Model):
    name = models.CharField(max_length=255, unique=True)
    numberOfSongs = models.IntegerField()

    def __str__(self) -> str:
        return str(self.name)


class Song(models.Model):
    track = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, unique=True)
    album = models.CharField(max_length=255)
    length = models.TimeField(default=datetime.time)
    playlist = models.ManyToManyField("Playlist")

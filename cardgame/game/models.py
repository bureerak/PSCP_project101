from django.db import models

# Create your models here.

class Room(models.Model):
    room_name = models.CharField(max_length=50, unique=True)
    max_members = models.PositiveIntegerField(default=4)  # Maximum number of members allowed
    current_members = models.PositiveIntegerField(default=0)  # Current number of members

    def __str__(self):
        return self.room_name

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f"{self.room} - {self.sender}"

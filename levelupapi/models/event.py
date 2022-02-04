from django.db import models

class Event(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='organizing')
    attendees = models.ManyToManyField("Gamer", through="Event_Gamer", related_name="attending")
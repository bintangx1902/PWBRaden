from django.db import models
from aspirasi.models import Aspiration
from django.contrib.auth.models import User


class Feedback(models.Model):
    staff_name = models.ForeignKey(User, on_delete=models.CASCADE)
    aspiration = models.ForeignKey(Aspiration, related_name='feedback', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='')
    feedback = models.TextField()

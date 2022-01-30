from django.db import models

# Create your models here.
from django.db import models

class Input(models.Model):
    input_text = models.CharField(max_length=250)

    def __str__(self):
        return self.input_text
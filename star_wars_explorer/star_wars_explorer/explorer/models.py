from django.db import models

# Create your models here.


class Collection(models.Model):
    csv_file = models.FileField(upload_to="files/")
    created = models.DateTimeField(auto_now_add=True)

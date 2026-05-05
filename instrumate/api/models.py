from django.db import models

# Create your models here.
    

class Movement(models.Model):
    name = models.TextField(primary_key=True)
    file = models.BinaryField()

    class Meta:
        managed = False
        app_label = 'movement'
        db_table = 'bvh_files'

from django.db import models

# Create your models here.

class JSONModel(models.Model):
	title = models.CharField('Назва', max_length=255)
	json_field = models.TextField('JSON field')

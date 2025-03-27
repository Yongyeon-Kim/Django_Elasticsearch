from django.db import models

class StandardDoc(models.Model):
    code_type = models.CharField(max_length=10)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    contents = models.TextField()

    def __str__(self):
        return f"{self.code_type} {self.code} {self.name}"
from django.db import models

class StandardDoc(models.Model):
    code_type = models.CharField(max_length=10)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    contents = models.TextField()

    name_en = models.CharField(max_length=255, blank=True, default="")
    contents_en = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.code_type} {self.code} {self.name}"
from django.db import models


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = '0', "Draft"
        PUBLISHED = '1', "Published"
        REMOVED = '2', "Removed"

    status = models.CharField(choices=Status.choices, max_length=1)

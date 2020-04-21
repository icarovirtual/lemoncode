class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = '0', "Draft"
        PUBLISHED = '1', "Published"
        REMOVED = '2', "Published"

    status = models.CharField(choices=Status, max_length=1)

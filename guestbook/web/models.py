from django.db import models

# Create your models here.
class Message(models.Model):
    user = models.CharField('Name', max_length = 50)
    subject = models.CharField('Subject', max_length = 200)
    content = models.TextField('content')
    publication_date = models.DateTimeField("MessageDate", auto_now_add = True)

    def __str__(self):
        return self.subject
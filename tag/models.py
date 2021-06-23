from django.db import models

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=32, verbose_name="태그명")
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")

    def __str__(self):
        return self.name

    def clean(self):
        """
        Custom validation (read docs)
        PS: why do you have null=True on charfield?
        we could avoid the check for name
        """
        if self.name:
            self.name = self.name.strip()

    class Meta:
        db_table = "tag table"
        verbose_name = "태그"
        verbose_name_plural = "태그"

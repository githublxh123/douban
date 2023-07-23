from django.db import models


class Book(models.Model):
    id = models.AutoField(primary_key=True)  # 将id字段设置为主键
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    image_url = models.TextField()
    publisher = models.CharField(max_length=255)
    publication_date = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    rating = models.FloatField()
    rating_count = models.CharField()
    quotes = models.TextField()

    class Meta:
        # 指定表名为 "books"
        db_table = 'books'
        managed = False



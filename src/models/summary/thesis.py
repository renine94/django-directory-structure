from django.db import models


class Thesis(models.Model):
    user = models.ForeignKey('src.User', on_delete=models.CASCADE, related_name='thesises', help_text='요청자')

    url = models.URLField('논문 PDF 요청 주소', default='')
    content = models.TextField('논문 요약 내용', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

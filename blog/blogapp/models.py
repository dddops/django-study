from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from utils.models import TimestampModel

User = get_user_model()

class Blog(models.Model):
  CATEGORY_CHOICES = (
    ('free', '자유'),
    ('travel', '여행'),
    ('cat', '고양이'),
    ('dog', '강아지'),
  )

  category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES, default='free')
  title = models.CharField('제목', max_length=100)
  content = models.TextField('본문')
  author = models.ForeignKey(User, on_delete=models.CASCADE)

  created_at = models.DateTimeField('작성일자', auto_now_add=True)
  updated_at = models.DateTimeField('수정일자', auto_now=True)

  class Meta:
    verbose_name = 'blog'
    verbose_name_plural = 'blog list'

  def __str__(self):
    return f'[{self.category}] {self.title}'

  def get_absolute_url(self):
    return reverse('blog:detail', kwargs={'blog_pk': self.pk})

class Comment(TimestampModel):
  blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
  content = models.CharField('본문', max_length=255)
  author = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
      return f'[{self.blog.category}] 댓글'

  class Meta:
    verbose_name = 'comment'
    verbose_name_plural = 'comment list'
    ordering = ['-created_at', '-id']
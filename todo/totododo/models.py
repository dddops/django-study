from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Todo(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField('제목',max_length=50)
  description = models.TextField('설명',)
  start_date = models.DateField('시작일',)
  end_date = models.DateField('마감일',)
  is_completed = models.BooleanField('완료여부',default=False)
  created_at = models.DateTimeField('생성일시',auto_now_add=True)
  modified_at = models.DateTimeField('수정일시',auto_now=True)

  def __str__(self):
    return self.title

  class Meta:
    verbose_name = 'Todo'
    verbose_name_plural = 'Todos'

  def get_absolute_url(self):
    from django.urls import reverse
    return reverse('todo:detail', kwargs={'pk': self.pk})
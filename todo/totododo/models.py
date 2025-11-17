from io import BytesIO

from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel

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

  image = models.ImageField('이미지', null=True, blank=True, upload_to='todo/%Y/%m/%d')
  thumbnail = models.ImageField('썸네일', null=True, blank=True, upload_to='todo/%Y/%m/%d/thumbnail')


  def __str__(self):
    return self.title

  class Meta:
    verbose_name = 'Todo'
    verbose_name_plural = 'Todos'

  def get_absolute_url(self):
    from django.urls import reverse
    return reverse('todo:detail', kwargs={'pk': self.pk})

  def get_thumbnail_image_url(self):
    if self.thumbnail:
      return self.thumbnail.url
    elif self.image:
      return self.image.url
    return None

  def save(self, *args, **kwargs):
    if not self.image or not self.image.name:
      self.thumbnail = None
      return super().save(*args, **kwargs)

    from PIL import Image
    image = Image.open(self.image)
    image.thumbnail((300, 300))

    from pathlib import Path
    image_path = Path(self.image.name)

    thumbnail_name = image_path.stem
    thumbnail_extension = image_path.suffix.lower()
    thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}'

    if thumbnail_extension in ['.jpg','.jpeg']:
      file_type = 'JPEG'
    elif thumbnail_extension in ['.gif']:
      file_type = 'GIF'
    elif thumbnail_extension in ['.png']:
      file_type = 'PNG'
    else:
      return super().save(*args, **kwargs)

    temp_thumb = BytesIO()
    image.save(temp_thumb, file_type)
    temp_thumb.seek(0)

    self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
    temp_thumb.close()
    return super().save(*args, **kwargs)



class Comment(TimeStampedModel):
 todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
 content = models.TextField('댓글', max_length=100)
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 created_at = models.DateTimeField(auto_now_add=True)

 class Meta:
    verbose_name = 'Comment'
    verbose_name_plural = 'Comments'
    ordering = ['-created_at']

 def __str__(self):
   return f'[{self.todo.title}] 댓글'

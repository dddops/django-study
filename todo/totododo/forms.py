from django import forms
from totododo.models import Todo, Comment


class TodoForm(forms.ModelForm):
  class Meta:
    model = Todo
    fields = ['title','description','start_date','end_date','is_completed']
    widgets = {
      'start_date': forms.SelectDateWidget(),
      'end_date': forms.SelectDateWidget(),
    }


class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ('content',)
    widgets = {
    'content': forms.Textarea(attrs={
    'rows': 4,
    'cols': 40,
    'class': 'form-control',
    'placeholder': '댓글을 입력하세요.',
    }),}

    lables = {
      'content': '댓글'
    }
from django import forms
from totododo.models import Todo

class TodoForm(forms.ModelForm):
  class Meta:
    model = Todo
    fields = ['title','description','start_date','end_date','is_completed']
    widgets = {
      'start_date': forms.SelectDateWidget(),
      'end_date': forms.SelectDateWidget(),
    }
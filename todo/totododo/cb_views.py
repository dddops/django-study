from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from totododo.forms import TodoForm
from totododo.models import Todo

class TodoListView (ListView):
  queryset = Todo.objects.all()
  template_name = 'todo_list.html'
  paginate_by = 10

class TodoDetailView (DetailView):
  model = Todo
  template_name = 'todo_detail.html'


class TodoCreateView (LoginRequiredMixin, CreateView):
  model = Todo
  template_name = 'todo_create.html'
  form_class = TodoForm

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    return HttpResponseRedirect(self.get_success_url())

  def get_success_url(self):
    return reverse_lazy('todo:detail', kwargs={'pk': self.object.pk})

class TodoUpdateView (LoginRequiredMixin, UpdateView):
  model = Todo
  template_name = 'todo_update.html'
  form_class = TodoForm

  def get_queryset(self):
    queryset = super().get_queryset()
    if self.request.user.is_superuser:
      return queryset
    return queryset.filter(user=self.request.user)

  def get_success_url(self):
    return reverse_lazy('todo:detail', kwargs={'pk':self.object.pk})


class TodoDeleteView (LoginRequiredMixin, DeleteView):
  model = Todo

  def get_queryset(self):
    queryset = super().get_queryset()
    if self.request.user.is_superuser:
      return queryset
    return queryset.filter(user=self.request.user)

  def get_success_url(self):
    return reverse_lazy('todo:list')
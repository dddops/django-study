from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from totododo.forms import TodoForm, CommentForm
from totododo.models import Todo, Comment


class TodoListView (ListView):
  queryset = Todo.objects.all()
  template_name = 'todo_list.html'
  paginate_by = 10

class TodoDetailView (LoginRequiredMixin, DetailView):
  model = Todo
  template_name = 'todo_detail.html'
  context_object_name = 'todo'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['comments'] = self.object.comment_set.all().order_by('-created_at')
    context['comment_form'] = CommentForm()
    return context

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


class CommentCreateView(LoginRequiredMixin,CreateView):
  model = Comment
  form_class = CommentForm

  def get(self, *args, **kwargs):
    raise Http404

  def form_valid(self, form):
    todo = self.get_todo()
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.todo = todo
    self.object.save()
    return HttpResponseRedirect(reverse_lazy('todo:detail', kwargs={'pk': todo.pk}))

  def get_todo(self):
    pk = self.kwargs.get('pk')
    todo = get_object_or_404(Todo, pk=pk)
    return todo

class CommentUpdateView (LoginRequiredMixin, UpdateView):
  model = Comment
  form_class = CommentForm

  def get_object(self, queryset=None):
    obj = super().get_object(queryset)

    if obj.user != self.request.user and not self.request.user.is_superuser:
      raise Http404("해당 댓글을 수정할 권한이 없습니다.")
    return obj

  def get_success_url(self):
    return reverse_lazy("todo:detail", kwargs={"pk": self.object.todo.id})


class CommentDeleteView (LoginRequiredMixin, DeleteView):
  model = Comment

  def get_object(self, queryset=None):
    obj = super().get_object(queryset)

    if obj.user != self.request.user and not self.request.user.is_superuser:
      raise Http404("해당 댓글을 삭제할 권한이 없습니다.")
    return obj

  def get_success_url(self):
    return reverse_lazy("todo:detail", kwargs={"pk": self.object.todo.id})
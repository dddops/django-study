from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from totododo.forms import TodoForm
from totododo.models import Todo
# Create your views here.

def todo_list(request):
  todos = Todo.objects.all().order_by('-created_at')
  context = {
    'todos' : todos,
    'count': todos.count()
  }
  return render(request, 'todo_list.html', context)

def todo_info(request, pk):
  todo = get_object_or_404(Todo,pk=pk)
  context = {
    'todo' : todo
  }
  return render(request, 'todo_info.html', context)


@login_required
def todo_create(request):
  form = TodoForm(request.POST or None)
  if form.is_valid():
    todo = form.save(commit=False)
    todo.user = request.user
    todo.save()
    return redirect(reverse('todo_info', kwargs={'pk' : todo.pk}))
  context = {
    'form' : form
  }
  return render(request, 'todo_create.html', context)

@login_required
def todo_update(request, pk):
  todo = get_object_or_404(Todo, pk=pk, user=request.user)
  form = TodoForm(request.POST or None, instance=todo)
  if form.is_valid():
    todo = form.save()
    return redirect(reverse('todo_info', kwargs={'pk' : todo.pk}))
  context = {
    'form' : form
  }
  return render(request, 'todo_update.html', context)

@require_http_methods(['POST'])
@login_required
def todo_delete(request, pk):
  todo = get_object_or_404(Todo, pk=pk, user=request.user)
  todo.delete()
  return redirect(reverse('todo_list'))

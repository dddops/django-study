from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blogapp.models import Blog

class BlogListView(ListView):
    # model = Blog
    queryset = Blog.objects.all().order_by('-created_at')
    template_name = 'blog_list.html'
    paginate_by = 10

    def get_queryset(self):
      queryset = super().get_queryset()
      q = self.request.GET.get('q')
      if q:
        queryset = queryset.filter(
          Q(title__icontains=q) |
          Q(description__icontains=q)
        )
      return queryset

class BlogDetailView(DetailView):
  model = Blog
  template_name = 'blog_detail.html'

  # def get_object(self):
  #   object = super().get_object()
  #   return object

class BlogCreateView(LoginRequiredMixin,CreateView):
  model = Blog
  template_name = 'blog_create.html'
  fields = ['category', 'title', 'content']

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.author = self.request.user
    self.object.save()
    return HttpResponseRedirect(self.get_success_url())

  def get_success_url(self):
    return reverse_lazy('blog: detail', kwargs={'pk':self.object.pk})


class BlogUpdateView(LoginRequiredMixin,UpdateView):
  model = Blog
  template_name = 'blog_update.html'
  fields = ['category', 'title', 'content']

  def get_queryset(self):
    queryset = super().get_queryset()
    if self.request.user.is_superuser:
      return queryset
    return queryset.filter(author=self.request.user)

  def get_success_url(self):
    return reverse_lazy('blog:detail', kwargs={'pk':self.object.pk})

class BlogDeleteView(LoginRequiredMixin,DeleteView):
  model = Blog

  def get_queryset(self):
    queryset = super().get_queryset()
    if not self.request.user.is_superuser:
      queryset = queryset.filter(author=self.request.user)
      return queryset
    return None

  def get_success_url(self):
    return reverse_lazy('blog:list')
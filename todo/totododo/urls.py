from django.urls import path
from totododo import cb_views

app_name = 'totododo'

urlpatterns = [
  path('',cb_views.TodoListView.as_view(),name='list'),
  path('<int:pk>/', cb_views.TodoDetailView.as_view(),name='detail'),
  path('create/', cb_views.TodoCreateView.as_view(),name='create'),
  path('<int:pk>/update/', cb_views.TodoUpdateView.as_view(),name='update'),
  path('<int:pk>/delete/', cb_views.TodoDeleteView.as_view(),name='delete'),
  path('<int:pk>/comment/create/', cb_views.CommentCreateView.as_view(),name='comment_create'),
  path('<int:pk>/comment/update/', cb_views.CommentUpdateView.as_view(),name='comment_update'),
  path('<int:pk>/comment/delete/', cb_views.CommentDeleteView.as_view(),name='comment_delete'),
]
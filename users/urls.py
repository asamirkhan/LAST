from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('registration/', views.UserCreateView.as_view(), name='registration'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('author/<pk>/', views.AuthorProfileView.as_view(), name='author_detail'),
    path('author/edit/<pk>/', views.AuthorEditView.as_view(), name='author_edit'),
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('new_reviwers/', views.ReviewersListView.as_view(), name='inactive_reviewers')
]

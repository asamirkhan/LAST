from django.urls import path

from . import views

urlpatterns = [
	path('/', views.PublicationListView.as_view(), name='publications'),
	path('unchecked/', views.PublicationListView.as_view(), name='unchecked'),
    path('noreviewer/', views.PublicationListView.as_view(), name='noreviewer'),
    path('mine/', views.PublicationListView.as_view(), name='mine'),
    path('for_reading/', views.PublicationListView.as_view(), name='for_reading'),
    path('create/', views.PublicationCreateView.as_view(), name='create'),
    path('add_comment/<pk>/', views.PublicationCommentView.as_view(), name='add_comment'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('add_to_reading/<pk>/', views.AddPublicationToReading.as_view(), name='add_to_reading'),
    path('remove_from_reading/<pk>/', views.RemovePublicationFromReading.as_view(), name='remove_from_reading'),
    path('edit/<pk>/', views.PublicationEditView.as_view(), name='edit'),
    path('<pk>/', views.PublicationDetailView.as_view(), name='detail'),
    path('delete/<pk>/', views.PublicationDeleteView.as_view(), name='delete'),
	path('delete_comment/<pk>/<publication_pk>/', views.PublicationCommentDeleteView.as_view(), name='delete_comment'),
	path('create_tag/<pk>/', views.CreateTagView.as_view(), name='create_tag'),
	path('add_tag/<pk>/', views.AddTagToPublicationView.as_view(), name='add_tag'),
]

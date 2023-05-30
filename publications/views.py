from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.base import View
from . import services
from .forms import (PublicationCreateFrom, PublicationReviewFrom,
                    PublicationCommentForm, PublicationTagForm,
                    TagCreateForm)
from .models import Publication, Category, PublicationComment, Tag


class MainView(View):

    def get(self, request):
        publications = services.filter_queryset(self.request)
        return render(
                request, 
                'main.html', 
                {'publications': publications}
            )


class PublicationListView(ListView):
    model = Publication
    template_name = 'publications/publications_list.html'
    context_object_name = 'publications'

    def get_queryset(self):
        return services.filter_queryset(self.request)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'mine' in self.request.path:
            queryset = self.get_queryset()
            context['avg_mark'] = services.aggregate_avg_mark(queryset)
            context['comments_count'] = services.count_author_comments(queryset)
        return context
    

class PublicationCreateView(View):
    def post(self, request):
        publication_form = PublicationCreateFrom(
            data=request.POST, files=request.FILES
            )
        
        if publication_form.is_valid():
            new_publication = publication_form.save(commit=False)
            new_publication.author = request.user
            new_publication.save()
            return redirect(new_publication.get_absolute_url() + "?tab=tags")
        return render(
                request, 
                'publications/create.html', 
                {'form': publication_form}
            )
    
    def get(self, request):
        publication_form = PublicationCreateFrom()
        return render(
                request, 
                'publications/create.html', 
                {'form': publication_form}
            )
    

class PublicationDetailView(DetailView):
    model = Publication
    template_name = 'publications/detail.html'
    context_object_name = 'publication'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publication = self.get_object()
        context['form'] = PublicationReviewFrom(
            instance=publication, 
            initial={'status': publication.is_accepted}
            )
        context['edit_form'] = PublicationCreateFrom(instance=publication)
        context['comment_form'] = PublicationCommentForm()
        context['tags_form'] = PublicationTagForm(instance=publication)
        context['create_tag_from'] = TagCreateForm()

        reviewers_comments = publication.comments.filter(author__is_reviewer=True)
        others_comments = publication.comments.exclude(author__is_reviewer=True)
        context['comments'] = [reviewers_comments, others_comments]
        return context
    
    def post(self, request, pk):
        publication = self.get_object()
        publication_form = PublicationReviewFrom(
            data=request.POST, instance=publication
            )
        if publication_form.is_valid():
            publication = publication_form.save(commit=False)
            if request.POST['status'] == 'True':
                publication.is_accepted = True
                publication.is_denied = False
            else:
                publication.is_accepted = False
                publication.is_denied = True
            publication.save()
            return redirect(publication.get_absolute_url())
        return render(
                request, 
                'publications/create.html', 
                {'form': publication_form}
            )
    
    def get(self, request, pk):
        services.set_reviewer(request.user, pk)
        return super().get(request)


class AddTagToPublicationView(View):
    def post(self, request, pk):
        publication = Publication.objects.get(pk=pk)
        form = PublicationTagForm(request.POST, instance=publication)
        if form.is_valid():
            form.save()
        print(form.errors)
        return redirect(publication.get_absolute_url() + "?tab=tags")


class CreateTagView(View):
    def post(self, request, pk):
        form = TagCreateForm(request.POST)
        publication = Publication.objects.get(pk=pk)
        tag_name = request.POST.get('name', '')
        tags = Tag.objects.filter(name=tag_name)

        if tags.exists():
            publication.tags.add(tags.first())
            return redirect(request.META['HTTP_REFERER'])
        if form.is_valid():
            new_tag = form.save()
            publication.tags.add(new_tag)
        return redirect(request.META['HTTP_REFERER'])


class PublicationCommentView(View):
    def post(self, request, pk):
        form = PublicationCommentForm(request.POST)
        if form.is_valid():
            publication = Publication.objects.get(pk=pk)
            comment = form.save(commit=False)
            comment.publication = publication
            comment.author = request.user
            comment.save()
            return redirect(publication.get_absolute_url() + "?tab=comments")


class PublicationCommentDeleteView(DeleteView):
    model = PublicationComment

    def get_success_url(self, **kwargs):
        return reverse('detail', kwargs={"pk": self.kwargs['publication_pk']})
        

class PublicationEditView(View):
    def post(self, request, pk):
        publication = Publication.objects.get(pk=pk)
        publication_form = PublicationCreateFrom(
            data=request.POST, files=request.FILES, instance=publication
            )
        if publication_form.is_valid():
            new_publication = publication_form.save(commit=False)
            new_publication.author = request.user
            publication.is_accepted = False
            publication.is_denied = False
            new_publication.save()
            return redirect(new_publication.get_absolute_url())
        return render(
                request, 
                'publications/detail.html', 
                {'edit_form': publication_form}
            )


class CategoryListView(ListView):
    model = Category
    template_name = 'categories/list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return super().get_queryset().filter(
                publication__is_accepted=True
            ).annotate(
                publications_count=Count('publication'),
            )
    

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publications'] = services.filter_queryset(
            self.request,
            category=self.get_object()
            )
        return context
    

class AddPublicationToReading(View):
    def get(self, request, pk):
        services.add_to_reading_list(request.user, pk)
        return redirect(request.META['HTTP_REFERER'])
    

class RemovePublicationFromReading(View):
    def get(self, request, pk):
        services.remove_from_reading_list(request.user, pk)
        return redirect(request.META['HTTP_REFERER'])


class PublicationDeleteView(DeleteView):
    model = Publication
    success_url = "/"

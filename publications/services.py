from django.db.models import Avg, Count, QuerySet

from .models import Publication, PublicationForReading, Tag


def filter_queryset(request, **kwargs) -> QuerySet:
	params = {'is_accepted': True, 'is_denied': False}

	if 'unchecked' in request.path:
		params = {'reviewer': request.user}
	if 'noreviewer' in request.path:
		params = {'reviewer__isnull': True}
	if 'mine' in request.path:
		params = {'author': request.user}
	if 'for_reading' in request.path:
		if hasattr(request.user, 'reading'):
			return request.user.reading.publications.all()
		return
	if request.GET.get('search'):
		qs = filter_queryset_for_search(request.GET['search'], params, kwargs)
		return qs
		# params['name__icontains'] = request.GET['search']

	return Publication.objects.filter(**params, **kwargs)
	

def filter_queryset_for_search(search: str, params: dict, kwargs: dict) -> QuerySet:
	tag = Tag.objects.filter(name=search)
	print(tag)
	if tag.exists():
		params['tags__in'] = tag
	else:
		params['name__icontains'] = search
	qs = Publication.objects.filter(
			**params, **kwargs
			)
	return qs


def aggregate_avg_mark(queryset):
	return queryset.aggregate(avg_mark=Avg('mark'))


def aggregate_author_qs(users):
	qs = users.annotate(avg_mark=Avg('publications__mark'))
	qs = qs.annotate(publications_count=Count('publications'))
	return qs


def count_author_comments(queryset):
	return queryset.aggregate(count=Count('comments'))


def add_to_reading_list(user, publication_pk):
	publication = Publication.objects.get(pk=publication_pk)
	if hasattr(user, 'reading'):
		bookmarks = user.reading
	else:
		bookmarks = PublicationForReading.objects.create(reader=user)
	bookmarks.publications.add(publication)


def remove_from_reading_list(user, publication_pk):
	publication = Publication.objects.get(pk=publication_pk)
	bookmarks = user.reading
	bookmarks.publications.remove(publication)


def set_reviewer(user, publication_pk):
	publication = Publication.objects.get(pk=publication_pk)
	if not publication.reviewer and user.is_reviewer and user.is_accepted:
		publication.reviewer = user
		publication.save()

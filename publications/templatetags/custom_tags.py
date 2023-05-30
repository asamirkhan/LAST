from django import template

from publications.models import Category

register = template.Library()


@register.simple_tag()
def check_publication_in_reading(user, publication):
	if hasattr(user, 'reading'):
		if publication in user.reading.publications.all():
			return True
	return False


@register.simple_tag()
def get_all_categories():
	return Category.objects.all()[:10]
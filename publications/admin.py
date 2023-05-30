from django.contrib import admin

from .models import Category, Publication, PublicationComment, Tag


class PublicationCommentInline(admin.TabularInline):
	model = PublicationComment
	extra = 0
	readonly_fields = ['text', 'created']

	
@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
	inlines = [PublicationCommentInline]
	list_display = [
		'name',
		'category',
		'mark',
		'author',
		'reviewer',
		'published',
		'is_accepted'
		]
	
	readonly_fields = [
		'name',
		'category',
		'mark',
		'author',
		'published',
		'document',
		'abstract'
		
	]
	filter_horizontal = ["tags"]
	
	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		field = super().formfield_for_foreignkey(db_field, request, **kwargs)
		if db_field.name == 'reviewer':
			field.queryset = field.queryset.exclude(pk=request.user.pk)  
		return field


admin.site.register(Category)
admin.site.register(Tag)

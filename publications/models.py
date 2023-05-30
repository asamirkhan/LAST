import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from pytils.translit import slugify

User = get_user_model()


class Category(models.Model):
	name = models.CharField('Название категории', max_length=120)

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'
	
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse("category_detail", kwargs={"pk": self.pk})


class Tag(models.Model):
	name = models.CharField('Название тэга', max_length=120, unique=True)
	slug = models.SlugField(blank=True, null=True)

	class Meta:
		verbose_name = 'Тэг'
		verbose_name_plural = 'Тэги'

	def __str__(self):
		return self.name

	def save(self):
		print(self.slug)
		print(slugify(self.name))
		if not self.slug:
			self.slug = slugify(self.name)
		super().save()
	

class Publication(models.Model):
	name = models.CharField('Название', max_length=120)
	published = models.DateField('Опубликовано', auto_now_add=True)
	is_denied = models.BooleanField('Отклонено', default=False)
	is_accepted = models.BooleanField('Подтверждено', default=False)
	abstract = models.TextField('Аннотация')
	mark = models.PositiveIntegerField(
		'Оценка', 
		blank=True, 
		null=True, 
		validators=[MaxValueValidator(10)]
		)
	document = models.FileField(
		'Документ', 
		upload_to='documents/',
		validators=[FileExtensionValidator(['pdf', 'txt', 'doc', 'docx'])]
		)
	category = models.ForeignKey(
		Category, 
		on_delete=models.CASCADE, 
		verbose_name='Категория'
		)
	author = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		verbose_name='Автор',
		related_name='publications'
	)
	reviewer = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		verbose_name='Рецензент',
		related_name='works',
		null=True,
		blank=True
	)
	tags = models.ManyToManyField(Tag, verbose_name="Тэги", blank=True, null=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("detail", kwargs={"pk": self.pk})
	
	def get_status(self):
		if self.is_accepted:
			return True
		elif self.is_denied:
			return False

	def save(self, **kwargs):
		if self.is_accepted and self.is_denied:
			raise ValidationError('Публикация не может быть одновременно Отклонена и Подтверждена!')
		super().save()
		if self.reviewer == None:
			channel_layer = get_channel_layer()
			data = {"link": self.get_absolute_url()}
			async_to_sync(channel_layer.group_send)(
				'notification_group', {
					'type': 'send_notification',
					'value': json.dumps(data)
				}
				
			)
		
	class Meta:
		verbose_name = 'Публикация'
		verbose_name_plural = 'Публикации'


class PublicationComment(models.Model):
	author = models.ForeignKey(
		User, 
		on_delete=models.CASCADE,
		blank=True,
		null=True
		)
	publication = models.ForeignKey(
		Publication, 
		on_delete=models.CASCADE,
		related_name='comments'
		)
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created']

	
class PublicationForReading(models.Model):
	reader = models.OneToOneField(
		User, 
		on_delete=models.CASCADE,
		related_name='reading'
		)
	publications = models.ManyToManyField(
		Publication, 
		related_name='publications_for_reading'
		)

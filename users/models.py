from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
	email = models.EmailField(verbose_name='E-mail')
	username = models.CharField(
		verbose_name='Имя пользователя', 
		max_length=100, 
		unique=True
		)
	is_reviewer = models.BooleanField(verbose_name='Рецензент', default=False)
	is_reader = models.BooleanField(verbose_name='Читатель', default=False)
	is_accepted = models.BooleanField('Одобрено', default=True)
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
	about_me = models.TextField(max_length=500, blank=True, null=True)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.username

	def get_absolute_url(self):
		return reverse("author_detail", kwargs={"pk": self.pk})

	def get_role(self):
		if not self.is_reviewer and not self.is_reader:
			return 'Автор'
		elif self.is_reviewer:
			return 'Рецензент'
		elif self.is_reader:
			return 'Читатель'

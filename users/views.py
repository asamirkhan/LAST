from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.base import View

from publications import services
from .forms import UserRegistrationForm, CustomAuthenticationForm, AuthorEditForm
from .models import CustomUser
from .services import save_user_type


class UserCreateView(View):

	def post(self, request):
		data = request.POST
		user_form = UserRegistrationForm(data)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			save_user_type(data, new_user)
			return redirect(reverse('login'))
		return render(
				request,
				'registration/registration.html',
				{'form': user_form}
			)

	def get(self, request):
		user_form = UserRegistrationForm()
		return render(
				request,
				'registration/registration.html',
				{'form': user_form}
			)


class CustomLoginView(LoginView):
	form_class = CustomAuthenticationForm


class AuthorListView(ListView):
	model = CustomUser
	template_name = 'users/authors_list.html'
	context_object_name = 'authors'

	def get_queryset(self):
		qs = services.aggregate_author_qs(CustomUser.objects.filter(publications__is_accepted=True))
		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if 'mine' in self.request.path:
			queryset = self.get_queryset()
			context['avg_mark'] = services.aggregate_avg_mark(queryset)
			context['comments_count'] = services.count_author_comments(queryset)
		return context


class ReviewersListView(ListView):
	model = CustomUser
	template_name = 'users/reviewers_list.html'
	context_object_name = 'reviewers'

	def get_queryset(self):
		return CustomUser.objects.filter(is_accepted=False, is_reviewer=True)

	def post(self, request):
		reviewer = CustomUser.objects.filter(id=request.POST.get('id'))
		if reviewer.exists():
			reviewer = reviewer.first()
			reviewer.is_accepted = True
			reviewer.save()
		return redirect(reverse('inactive_reviewers'))


class AuthorProfileView(DetailView):
	model = CustomUser
	template_name = 'users/profile.html'
	context_object_name = 'author'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		publications = self.object.publications.filter(is_accepted=True)
		context['avg_mark'] = services.aggregate_avg_mark(publications)
		context['publications'] = publications
		return context


class AuthorEditView(View):
	def get(self, request, pk):
		user_form = AuthorEditForm(instance=request.user)
		return render(request, 'users/author_edit.html', {'form': user_form})

	def post(self, request, pk):
		user_form = AuthorEditForm(data=request.POST, files=request.FILES, instance=request.user)
		if user_form.is_valid():
			user_form.save()
			user = CustomUser.objects.get(pk=pk)
			return redirect(user.get_absolute_url())
		return render(
			request,
			'users/author_edit.html',
			{'form': user_form}
		)


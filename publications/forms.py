from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Publication, PublicationComment, Tag


class PublicationCreateFrom(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('name', 'category', 'document', 'abstract')
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "abstract": forms.Textarea(attrs={"class": "form-control"})
        }


class PublicationReviewFrom(forms.ModelForm):
    STATUSES = ((True, 'Подтверждено'),(False, 'Отклонено'),)
    status = forms.ChoiceField(choices=STATUSES, label='Статус', required=True)
    MARKS = [(i, i) for i in range(1, 11)][::-1]
    mark = forms.ChoiceField(choices=MARKS, label='Оценка', required=True, widget=forms.RadioSelect())

    class Meta:
        model = Publication
        fields = ('mark', 'status')


class PublicationCommentForm(forms.ModelForm):

    class Meta:
        model = PublicationComment
        fields = ('text',)
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control"})
        }


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)


class PublicationTagForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        label="Тэги",
        widget=FilteredSelectMultiple("Тэги", is_stacked=False),
        required=False
        )
    class Meta:
        model = Publication
        fields = ('tags',)
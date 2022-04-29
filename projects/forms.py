
from django.forms import ModelForm
from django import forms
from .models import Project, Query, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote (\'up\' for up vote), (\'down\' for down vote)',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class QueryForm(ModelForm):
    class Meta:
        model = Query
        fields = ['title', 'description','project']

        labels = {
            'value': 'Please Enter the Title of your query.',
            'description': 'Describe your needs here.'
        }
        widgets = {
            'project': forms.RadioSelect(),
        }
    def __init__(self, *args, **kwargs):
        super(QueryForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


     
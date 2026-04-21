from django import forms

from projects.models import Project
from team_finder.validators import validate_repository_url


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')

    def clean_github_url(self):
        return validate_repository_url(self.cleaned_data.get('github_url'))

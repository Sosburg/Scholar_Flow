from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Paper, Statement, Theme

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class PaperUploadForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ["title", "author", "year", "pdf"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Paper title"}),
            "author": forms.TextInput(attrs={"placeholder": "Author"}),
            "year": forms.TextInput(attrs={"placeholder": "Year"}),
        }

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ["name", "color"]

class StatementForm(forms.ModelForm):
    theme_ids = forms.ModelMultipleChoiceField(queryset=Theme.objects.none(), required=False, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Statement
        fields = ["text", "page_number", "note", "theme_ids"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
            "note": forms.Textarea(attrs={"rows": 3}),
        }
    def __init__(self, *args, workspace=None, **kwargs):
        super().__init__(*args, **kwargs)
        if workspace is not None:
            self.fields["theme_ids"].queryset = workspace.themes.all()

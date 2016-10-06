from django import forms

class RepositoryForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, required=True)


class AddStatementsForm(forms.Form):
    file = forms.FileField()


class QueryRepositoryForm(forms.Form):
    query = forms.CharField(label='Query', max_length=500, required=True)
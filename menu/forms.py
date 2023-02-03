from django import forms

from menu.models import Category


#  Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','description']
        
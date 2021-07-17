from django import forms
from .models import *

class StockCreateForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['category', 'item_name', 'quantity']
		
	# Validation
	def clean_category(self):
		category = self.cleaned_data.get('category')
		item_name = self.cleaned_data.get('item_name') #Modified to make sure one category can have multiple items
		if not category:
			raise forms.ValidationError('This field is required!')

		for instance in Stock.objects.all():
			if instance.category == category and instance.item_name == item_name:
				raise forms.ValidationError('Category' + str(category) + ' already has ' + str(item_name) + 
					'item, Add another item.')
		return category

	def clean_item_name(self):
		item_name = self.cleaned_data.get('item_name')
		if not item_name:
			raise forms.ValidationError('This field is required!')
		return item_name

class StockSearchForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['category','item_name']

	def __init__(self, *args, **kwargs):#Code to remove the required field asterisk from category
		super(StockSearchForm, self).__init__(*args, **kwargs)

		for key in self.fields:
			self.fields[key].required = False 

class StockUpdateForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['category', 'item_name', 'quantity']


class IssueForm(forms.ModelForm):
	class Meta:
		model = Stock 
		fields = ['issue_quantity', 'issue_to']

class ReceiveForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['receive_quantity']

class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level']

class StockHistorySearchForm(forms.ModelForm):
	start_date = forms.DateTimeField(required=False)
	end_date = forms.DateTimeField(required=False)

	class Meta:
		model = StockHistory
		fields = ['category', 'item_name', 'start_date', 'end_date']

	def __init__(self, *args, **kwargs):  
		super(StockHistorySearchForm, self).__init__(*args, **kwargs)
		for key in self.fields:
			self.fields[key].required = False 
	
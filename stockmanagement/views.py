from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
	title = 'Welocome, this is index page'
	form = "This is home page"
	context = {
	    "title": title,
	    "form":form,
	}

	#return render(request, "home.html", context)
	return redirect("/list_items")

@login_required
def list_items(request):
	header = 'List of items'
	form = StockSearchForm(request.POST or None)
	queryset = Stock.objects.all()
	context = {
	    "form": form,
	    "header": header,
	    "queryset": queryset,
	}
	#Searching an item and category
	if request.method == 'POST':
		queryset = Category.objects.all(#name__icontains=form['category'].value(),
                                        #stock__item_name__icontains=form['item_name'].value()
			)
		context = {
		   "form": form,
		   "header": header,
		   "queryset": queryset,
		}

	return render(request, "list_items.html", context)

@login_required
def add_items(request):
	form = StockCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, 'Successfully saved')
		return redirect('/list_items')
	context = {
		"form": form,
		"title": "Add Item"
	}
	return render(request, "add_items.html", context)

# Handling form updating.
@login_required
def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)

		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully updated')
			return redirect('/list_items')

	context = {
	     'form': form
	}
	return render(request, 'add_items.html', context)

# Delete view
@login_required
def delete_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, 'Successfully deleted')
		return redirect('/list_items')
	return render(request, 'delete_items.html')

# Details page view
def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	#queryset = get_object_or_404(Stock, pk=id)
	context = {
	     "queryset": queryset,
	}
	return render(request, "stock_detail.html", context)

# Issue and receive items views
def issue_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = IssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.receive_quantity = 0 #For trigger function in DB
		instance.quantity -= instance.issue_quantity
		instance.issue_by = str(request.user) # Displaying the currently logged in user
		instance.save()
		#instance.issue_by = str(request.user)
		messages.success(request, "Issued successfully!" +" "+ str(instance.quantity) + 
			" " + str(instance.item_name) + "s now left in the store.")

		return redirect('/stock_detail/' + str(instance.id))

	context = {
	    "title":'Issue' + str(queryset.item_name),
	    "queryset": queryset,
	    "form": form,
	    "username": 'Issued by:' + str(request.user)
	}
	return render(request, "add_items.html", context)

def receive_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.issue_quantity = 0 # For trigger function in DB
		instance.quantity += instance.receive_quantity
		instance.receive_by = str(request.user)
		instance.save()
		#instance.received_by = str(request.user)
		messages.success(request, "Received successfully!" +" "+ str(instance.quantity) + 
			" " + str(instance.item_name) + "s now left in the store.")

		return redirect('/stock_detail/' + str(instance.id))

	context = {
	    "title":'Received' + str(queryset.item_name),
	    "queryset": queryset,
	    "form": form,
	    "username": 'Received by:' + str(request.user)
	}
	return render(request, "add_items.html", context)

# Reorder-level view
def reorder_level(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.item_name) +
		 "is updated to " + str(instance.reorder_level))

		return redirect("/list_items")
	context = {
                  "instance": queryset,
                  "form": form,
	          }
	return render(request, "add_items.html", context)

@login_required
def list_history(request):
	header = 'History information'
	queryset = StockHistory.objects.all()
	form = StockHistorySearchForm(request.POST or None)
	context = {
	     "form": form,
	     "header": header,
	     "queryset": queryset,
	}

	#Searching code
	if request.method == 'POST':
		category = form['category'].value()
		queryset = StockHistory.objects.filter(
			item_name__icontains=form['item_name'].value(), 
			last_updated__range=[
			           form['start_date'].value(), 
			           form['end_date'].value()
			]
			)

		if (category != ''):
			queryset = queryset.filter(category_id=category)

		context = {
		  "form": form,
		  "header": header,
		  "queryset": queryset,
		}

	return render(request, "list_history.html", context)
from django.shortcuts import redirect
from django.shortcuts import render

from lists.models import Item


def home_view(request):
    return render(request, 'home.html')

def create_new_list_view(request):
	Item.objects.create(text=request.POST['item_text'])
	return redirect('/lists/the-only-list-in-the-world/')

def list_view(request):
	items = Item.objects.all()
	return render(request, 'list.html', {'items': items})

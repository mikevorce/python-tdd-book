from django.shortcuts import redirect
from django.shortcuts import render

from lists.models import Item, List


def home_view(request):
    return render(request, 'home.html')

def create_new_list_view(request):
	todo_list = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=todo_list)
	return redirect(f'/lists/{todo_list.id}/')

def list_view(request, list_id):
	todo_list = List.objects.get(id=list_id)
	return render(request, 'list.html', {'list': todo_list})

def add_todo_view(request, list_id):
	todo_list = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=todo_list)
	return redirect(f'/lists/{todo_list.id}/')

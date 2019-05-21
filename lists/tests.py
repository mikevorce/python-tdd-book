from django.test import TestCase

from lists.models import Item, List


class HomePageTest(TestCase):

    def test_root_uses_home_page_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class ListAndItemModelsTest(TestCase):
    
    def test_can_save_and_retrieve_items(self):
        todo_list = List()
        todo_list.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = todo_list
        first_item.save()

        second_item = Item()
        second_item.text = 'Ye olde second item'
        second_item.list = todo_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, todo_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, todo_list)
        self.assertEqual(second_saved_item.text, 'Ye olde second item')
        self.assertEqual(second_saved_item.list, todo_list)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        todo_list = List.objects.create()
        Item.objects.create(text='The first list item', list=todo_list)
        Item.objects.create(text='The second list item', list=todo_list)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'The first list item')
        self.assertContains(response, 'The second list item')

class CreateNewListViewTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/create-new-list', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/create-new-list', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


MAX_WAIT = 10  # maximum amount of time we're prepared to wait for tests

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # utility functions for tests -------------------------------------
    def wait_for_row_in_todo_list(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    # test functions --------------------------------------------------
    def test_can_start_a_list_for_one_user(self):
        # Kirsten goes to check out the homepage of the to-do app
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item immediately
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )   

        # She types "Buy peacock feathers" into a text box (Kirsten's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits <enter>, the page updates, and now the page lists
        # "1: Buy peacock feather" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_todo_list('1: Buy peacock feathers')        

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_todo_list('1: Buy peacock feathers',)
        self.wait_for_row_in_todo_list('2: Use peacock feathers to make a fly')

        # Satisfied, she closes her browser and goes off to daydream about her 
        # next fly-fishing lure design

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Kirsten starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_todo_list('1: Buy peacock feathers')

        # She notices that her list has a unique URL
        kirstens_list_url = self.browser.current_url
        self.assertRegex(kirstens_list_url, '/lists/.+')

        # Now dave hears about how awesome this to-do list app is from
        # kirsten and he wants to start a list too

        ## We do our best to simulate two different users by starting a
        ## new browser session to make sure that no information about
        ## kirsten's list is coming through cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Dave visits the homepage. He does not see kirsten's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)

        # Dave starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_todo_list('1: Buy milk')

        # Dave, like kirsten, notices his list has a unique URL
        daves_list_url = self.browser.current_url
        self.assertRegex(daves_list_url, '/lists/.+')
        self.assertNotEqual(daves_list_url, kirstens_list_url)

        # There is still no trace of kirsten's list items in dave's list 
        # after dave adds an item to his list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go about their lives

    def test_layaout_and_styling(self):
        # kirsten goes to the homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # she notices the box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10
        )

        # she starts a new list and sees the input is centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_todo_list('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10
        )
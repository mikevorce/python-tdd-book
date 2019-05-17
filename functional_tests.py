from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Kirsten goes to check out the homepage of the to-do app
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('This test is not complete. Finish it!')

        # She is invited to enter a to-do item immediately

        # She types "Buy peacock feathers" into a text box (Kirsten's hobby
        # is tying fly-fishing lures)

        # When she hits <enter>, the page updates, and now the page lists
        # "1: Buy peacock feather" as an item in a to-do list

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly"

        # The page updates again, and now shows both items on her list

        # Kirsten wonders whether the siter will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL... her to-do list is still there!

        # Satisfied, she closes her browser and goes off to daydream about her 
        # next fly-fishing lure design


if __name__ == '__main__':
    unittest.main(warnings='ignore')


"""Views tests."""

# from django.test import StaticLiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumTestCase(StaticLiveServerTestCase):
    """LiveServerTestCase subclass suited for Selenium tests."""

    timeout = 10
    _browsers = {
        'safari': webdriver.Safari,
        'firefox': webdriver.Firefox,
        'chrome': webdriver.Chrome,
    }
    driver = 'firefox'

    def setUp(self):
        self.browser = self._browsers.get(self.driver)()
        self.wait = WebDriverWait(self.browser, self.timeout)
        super().setUp()

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def find_css(self, selector):
        return self.browser.find_element_by_css_selector(selector)

    def get(self, url):
        self.browser.get(self.live_server_url + url)


class TestAuthentication(SeleniumTestCase):
    """Test that a user can login and logout."""

    driver = 'safari'

    def logs_in(self):
        user = User.objects.create_user(
            username='bernard',
            password='onions88',
            first_name='Bernard',
            last_name='Dupont')
        username = self.find_css('#id_username')
        password = self.find_css('#id_password')
        login_btn = self.find_css('#login')

        username.send_keys('bernard')
        password.send_keys('onions88')
        login_btn.click()

        self.wait.until(lambda _: 'index' in self.browser.current_url)
        self.assertIn('Bienvenue sur le site interne, {}'
                      .format(user.get_full_name()),
                      self.browser.page_source)

    def logs_out(self):
        profile_link = self.find_css('#profile')
        logout_link = self.find_css('#logout')

        profile_link.click()
        self.assertTrue(logout_link.is_displayed())
        logout_link.click()

        self.wait.until(lambda _: 'logout' in self.browser.current_url)

    def test(self):
        self.get('')
        self.logs_in()
        self.logs_out()

"""Functional website tests using Selenium."""

from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException


class CustomWebDriver(webdriver.Safari):
    """Our own WebDriver with some helpers added."""

    def find_css(self, css_selector):
        """Shortcut to find elements by CSS.

        Returns either a list or singleton.
        """
        elems = self.find_elements_by_css_selector(css_selector)
        found = len(elems)
        if found == 1:
            return elems[0]
        elif not elems:
            raise NoSuchElementException(css_selector)
        return elems

    def wait_css(self, css_selector, timeout=7):
        """Shortcut for WebDriverWait."""
        return WebDriverWait(self, timeout).until(
            lambda driver: driver.find_css(css_selector))


class SeleniumTestCase(StaticLiveServerTestCase):
    """LiveServerTestCase subclass suited for Selenium tests."""

    def setUp(self):
        self.wd = CustomWebDriver()
        super().setUp()

    def tearDown(self):
        self.wd.quit()
        super().tearDown()

    def get(self, url):
        self.wd.get(self.live_server_url + url)


class TestLogin(SeleniumTestCase):
    """User logs in."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='bernard',
            password='onions88',
            first_name='Bernard',
            last_name='Dupont')
        super().setUp()

    def login(self):
        username = self.wd.find_css('#id_username')
        password = self.wd.find_css('#id_password')
        login_btn = self.wd.find_css('#login')

        username.send_keys('bernard')
        password.send_keys('onions88')
        login_btn.click()
        self.wd.wait_css('#profile')

    def test_login(self):
        self.get('')
        self.login()
        self.assertTrue(self.user.is_authenticated())


class TestLogout(SeleniumTestCase):
    """User logs out."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='bernard',
            password='onions88',
            first_name='Bernard',
            last_name='Dupont')
        super().setUp()

    login = TestLogin.login

    def logout(self):
        profile_link = self.wd.find_css('#profile')
        profile_link.click()

        logout_btn = self.wd.find_css('#logout')
        logout_btn.click()
        self.wd.wait_css('.login-form')

    def test_logout(self):
        self.get('')
        self.login()
        self.logout()


class TestRegisterStudent(SeleniumTestCase):
    """User registers as student."""

    def setUp(self):
        super().setUp()

    def to_register_page(self):
        register_link = self.wd.find_css('#register')
        register_link.click()
        self.wd.wait_css('.register-form')

    def submit_register_details(self):
        first_name = self.wd.find_css('#id_first_name')
        last_name = self.wd.find_css('#id_last_name')
        email = self.wd.find_css('#id_email')
        password = self.wd.find_css('#id_password')
        role = Select(self.wd.find_css('#id_role'))
        register_btn = self.wd.find_css('#register')

        first_name.send_keys('Bernard')
        last_name.send_keys('Leduc')
        email.send_keys('bernard.leduc@example.net')
        password.send_keys('onions88')
        role.select_by_visible_text('Lycéen')
        register_btn.click()
        self.wd.wait_css('.compl-form')

    def test_register(self):
        self.get('')
        self.to_register_page()
        self.submit_register_details()

"""Functional website tests using Selenium."""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException

from .models import HighSchool, Country, Level, Branch


class CustomWebDriver(webdriver.Firefox):
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
        self.wait = WebDriverWait(self.wd, 7)
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
        self.wd.wait_css('#login-form')

    def test_logout(self):
        self.get('')
        self.login()
        self.logout()


class TestRegisterStudent(SeleniumTestCase):
    """User registers as student."""

    def setUp(self):
        HighSchool.objects.create(name="Lycée de l'Escaut")
        Country.objects.create(name='France')
        Level.objects.create(name='Terminale')
        Branch.objects.create(name='Scientifique', short_name='S')
        super().setUp()

    def go_to_register_page(self):
        self.get('')
        register_link = self.wd.find_css('#register')
        register_link.click()
        self.wd.wait_css('#register-form')

    def submit_register_details(self):
        first_name = self.wd.find_css('#id_first_name')
        last_name = self.wd.find_css('#id_last_name')
        email = self.wd.find_css('#id_email')
        password = self.wd.find_css('#id_password')
        role = Select(self.wd.find_css('#id_role'))

        first_name.send_keys('Bernard')
        last_name.send_keys('Leduc')
        email.send_keys('bernard.leduc@example.net')
        password.send_keys('onions88')
        role.select_by_visible_text('Lycéen')

        self.wd.find_css('#register').click()
        self.wd.wait_css('#info-form')

    def submit_student_info(self):
        line1 = self.wd.find_css('#id_line1')
        post_code = self.wd.find_css('#id_post_code')
        city = self.wd.find_css('#id_city')
        country = Select(self.wd.find_css('#id_country'))
        high_school = Select(self.wd.find_css('#id_high_school'))
        level = Select(self.wd.find_css('#id_level'))
        branch = Select(self.wd.find_css('#id_branch'))

        line1.send_keys('3 place des Mocassins')
        post_code.send_keys('13500')
        city.send_keys('Colmart')
        country.select_by_visible_text("France")
        high_school.select_by_visible_text("Lycée de l'Escaut")
        level.select_by_visible_text('Terminale')
        branch.select_by_visible_text('Scientifique')
        self.wd.find_css('#finish').click()
        self.wd.wait_css('#login-form')

    def test_register(self):
        self.go_to_register_page()
        self.submit_register_details()
        self.submit_student_info()

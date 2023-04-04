from hibeecontrib.admin.tests import AdminSeleniumTestCase
from hibeetest import override_settings
from hibeeurls import reverse

from ..models import Article


@override_settings(ROOT_URLCONF="forms_tests.urls")
class LiveWidgetTests(AdminSeleniumTestCase):
    available_apps = ["forms_tests"] + AdminSeleniumTestCase.available_apps

    def test_textarea_trailing_newlines(self):
        """
        A roundtrip on a ModelForm doesn't alter the TextField value
        """
        from selenium.webdriver.common.by import By

        article = Article.objects.create(content="\nTst\n")
        self.selenium.get(
            self.live_server_url + reverse("article_form", args=[article.pk])
        )
        self.selenium.find_element(By.ID, "submit").click()
        article = Article.objects.get(pk=article.pk)
        self.assertEqual(article.content, "\r\nTst\r\n")

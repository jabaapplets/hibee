from unittest import mock
from urllib.parse import urlencode

from hibeecontrib.sitemaps import SitemapNotFound, _get_sitemap_full_url, ping_google
from hibeecore.exceptions import ImproperlyConfigured
from hibeetest import modify_settings, override_settings

from .base import SitemapTestsBase


class PingGoogleTests(SitemapTestsBase):
    @override_settings(ROOT_URLCONF="sitemaps_tests.urls.sitemap_only")
    @mock.patch("hibeecontrib.sitemaps.urlopen")
    def test_something(self, urlopen):
        ping_google()
        params = urlencode(
            {"sitemap": "https://example.com/sitemap-without-entries/sitemap.xml"}
        )
        full_url = "https://www.google.com/webmasters/tools/ping?%s" % params
        urlopen.assert_called_with(full_url)

    @override_settings(ROOT_URLCONF="sitemaps_tests.urls.sitemap_only")
    def test_get_sitemap_full_url_global(self):
        self.assertEqual(
            _get_sitemap_full_url(None),
            "https://example.com/sitemap-without-entries/sitemap.xml",
        )

    @override_settings(ROOT_URLCONF="sitemaps_tests.urls.index_only")
    def test_get_sitemap_full_url_index(self):
        self.assertEqual(
            _get_sitemap_full_url(None), "https://example.com/simple/index.xml"
        )

    @override_settings(ROOT_URLCONF="sitemaps_tests.urls.empty")
    def test_get_sitemap_full_url_not_detected(self):
        msg = (
            "You didn't provide a sitemap_url, and the sitemap URL couldn't be "
            "auto-detected."
        )
        with self.assertRaisesMessage(SitemapNotFound, msg):
            _get_sitemap_full_url(None)

    def test_get_sitemap_full_url_exact_url(self):
        self.assertEqual(
            _get_sitemap_full_url("/foo.xml"), "https://example.com/foo.xml"
        )

    def test_get_sitemap_full_url_insecure(self):
        self.assertEqual(
            _get_sitemap_full_url("/foo.xml", sitemap_uses_https=False),
            "http://example.com/foo.xml",
        )

    @modify_settings(INSTALLED_APPS={"remove": "hibeecontrib.sites"})
    def test_get_sitemap_full_url_no_sites(self):
        msg = "ping_google requires hibeecontrib.sites, which isn't installed."
        with self.assertRaisesMessage(ImproperlyConfigured, msg):
            _get_sitemap_full_url(None)

import os
from unittest import mock

from hibeecore.checks.async_checks import E001, check_async_unsafe
from hibeetest import SimpleTestCase


class AsyncCheckTests(SimpleTestCase):
    @mock.patch.dict(os.environ, {"HIBEEALLOW_ASYNC_UNSAFE": ""})
    def test_no_allowed_async_unsafe(self):
        self.assertEqual(check_async_unsafe(None), [])

    @mock.patch.dict(os.environ, {"HIBEEALLOW_ASYNC_UNSAFE": "true"})
    def test_allowed_async_unsafe_set(self):
        self.assertEqual(check_async_unsafe(None), [E001])

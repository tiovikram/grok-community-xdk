"""Optional smoke tests against xAI's live API.

These tests run only when XAI_API_KEY is present. They intentionally use
read-only discovery endpoints so a normal test run does not create billable
generation jobs.
"""

import os
import unittest

from xai_grok import Grok


@unittest.skipUnless(os.environ.get("XAI_API_KEY"), "XAI_API_KEY is not configured")
class TestAPIIntegration(unittest.TestCase):
    def setUp(self):
        self.grok = Grok(os.environ["XAI_API_KEY"])

    def test_api_key(self):
        self.assertTrue(self.grok.api_key().api_key_id)

    def test_me(self):
        self.assertIsNotNone(self.grok.me())

    def test_models(self):
        self.assertIsInstance(self.grok.models().data, list)

    def test_language_models(self):
        self.assertIsInstance(self.grok.language_models().models, list)

    def test_embedding_models(self):
        self.assertIsInstance(self.grok.embedding_models().models, list)

    def test_image_generation_models(self):
        self.assertIsInstance(self.grok.image_generation_models().models, list)

    def test_video_generation_models(self):
        self.assertIsInstance(self.grok.video_generation_models().models, list)

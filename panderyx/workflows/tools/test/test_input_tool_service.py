from unittest import mock
from django.test import TestCase

from panderyx.workflows.test.factories import WorkflowFactory
from panderyx.workflows.tools.services.input_tools import InputUrlService


class TestInputUrlService(TestCase):
    def setUp(self):
        self.workflow = WorkflowFactory.build()

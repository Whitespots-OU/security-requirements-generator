from django.contrib.auth import get_user_model
from django.test import RequestFactory
from rest_framework.test import APITestCase

from apps.common.base_test import BaseTest

__all__ = ["BaseApiTest"]


User = get_user_model()


class BaseApiTest(APITestCase, BaseTest):
    def assertResponseStatus(self, response, status_code):
        if response.status_code != status_code:
            self.fail(f"Status code is not {status_code}. It's {response.status_code}")

    def assertListInResponse(self, serializer_class, qset, response, context_user: User = None):
        self.assertIn("results", response.data)

        context = self._get_request_context(context_user)
        serializer = serializer_class(many=True, instance=qset, context=context)
        self.assertEquals(len(serializer.data), len(response.data["results"]))
        self.assertListEqual(list(serializer.data), response.data["results"])

    def assertRetrieveInResponse(self, serializer_class, instance, response, context_user: User = None):
        context = self._get_request_context(context_user)
        serializer = serializer_class(instance=instance, context=context)
        self.assertDictEqual(serializer.data, response.data)

    def _get_request_context(self, user=None):
        context = {}
        if user:
            request = RequestFactory()
            request.user = user
            context["request"] = request
        return context

from unittest.mock import patch, MagicMock

from django.urls import reverse
from django_dynamic_fixture import G

from apps.api.base_test import BaseApiTest
from apps.common.utils import get_object_or_none
from apps.requirement.models import Category, Requirement, ExportRequest


@patch("apps.requirement.tasks.generate_pdf.send")
class CreateExportRequestTest(BaseApiTest):
    _url: str

    def setUp(self):
        super(CreateExportRequestTest, self).setUp()

        self._url = reverse("api_v1:request_export-create")

    def test_success(self, m_send: MagicMock):
        G(Category)
        category: Category = G(
            Category, name_en="name en", summary_en="summary en", name_ru="name ru", summary_ru="summary ru"
        )
        requirements_ids = []
        for i in range(3):
            requirement: Requirement = G(
                Requirement,
                categories=[category],
                title_en="title en",
                title_ru="title ru",
                summary_en="summary en",
                summary_ru="summary ru",
                text_en="text en",
                text_ru="text ru"
            )
            requirements_ids.append(requirement.id)
        requirements_ids.append(G(Requirement).id)

        post_data = {"data": [{"category_id": category.id, "requirements_ids": requirements_ids}]}
        response = self.client.post(self._url, data=post_data)
        self.assertEquals(response.status_code, 201)

        data = response.json()
        self.assertIn("uuid", data)
        export_request: ExportRequest = get_object_or_none(ExportRequest, uuid=data["uuid"])
        self.assertIsNotNone(export_request)

        self.assertEquals(export_request.status, ExportRequest.STATUS.CREATED)
        self.assertListEqual(export_request.data, post_data["data"])

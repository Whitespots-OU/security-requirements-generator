from unittest.mock import patch, MagicMock
from uuid import uuid4

from django_dynamic_fixture import G

from apps.common.base_test import BaseTest
from apps.common.utils import get_object_or_none
from apps.requirement.models import Category, Requirement, ExportRequest
from apps.requirement.tasks import generate_pdf


@patch("subprocess.run")
class CreateExportRequestTest(BaseTest):
    def test_success(self, m_run: MagicMock):
        category: Category = G(Category)
        requirements_ids = []
        for i in range(3):
            requirement: Requirement = G(Requirement, categories=[category])
            requirements_ids.append(requirement.id)
        requirements_ids.append(G(Requirement).id)

        data = [{"category_id": category.id, "requirements_ids": requirements_ids}]
        export: ExportRequest = G(ExportRequest, data=data)

        generate_pdf(str(export.uuid))

        self.assertEquals(m_run.call_count, 1)

        export: ExportRequest = get_object_or_none(ExportRequest, pk=export.pk)
        self.assertTrue(bool(export.file))
        self.assertEquals(export.status, ExportRequest.STATUS.FINISHED)

    def test_not_exists(self, m_run: MagicMock):
        generate_pdf(str(uuid4()))

        self.assertFalse(m_run.called)

    def test_failed(self, m_run: MagicMock):
        export: ExportRequest = G(ExportRequest, data=[])

        m_run.side_effect = Exception
        with self.assertRaises(Exception):
            generate_pdf(str(export.uuid))

        self.assertEquals(m_run.call_count, 1)

        export: ExportRequest = get_object_or_none(ExportRequest, pk=export.pk)
        self.assertEquals(export.status, ExportRequest.STATUS.FAILED)

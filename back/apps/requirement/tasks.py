import logging
import os
import subprocess
from tempfile import NamedTemporaryFile

import dramatiq

from django.conf import settings
from django.template import loader
from django.utils import translation

from apps.common.utils import get_object_or_none
from apps.requirement.models import ExportRequest, Category, Requirement
from apps.common.models import AssessmentButton, AdditionalLogo

__all__ = ["generate_pdf"]

logger = logging.getLogger(__name__)


@dramatiq.actor
def generate_pdf(uuid: str) -> None:
    export_request: ExportRequest = get_object_or_none(ExportRequest, uuid=uuid)
    if not export_request:
        return logger.warning(f"ExportRequestUUID={uuid} was not found at generate_pdf function")

    export_request.status = ExportRequest.STATUS.STARTED
    export_request.save(update_fields=["status"])

    with translation.override(export_request.language):
        categories = []
        for cat_data in export_request.data:
            category: Category = get_object_or_none(Category, id=cat_data["category_id"])
            if not category:
                message = f"CategoryID={cat_data['category_id']} was not found. ExportRequestUUID={export_request.uuid}"
                logger.warning(message)

                continue

            requirements_ids = cat_data.get("requirements_ids", [])
            categories.append(
                {
                    "category": category,
                    "requirements": Requirement.objects.filter(categories__in=[category]),
                    "selected_ids": requirements_ids,
                }
            )

        with NamedTemporaryFile(suffix=".html", delete=False) as f:
            try:
                export_dir = f"{settings.MEDIA_ROOT}/exports/"
                if not os.path.exists(export_dir):
                    os.mkdir(export_dir)

                template = loader.get_template("export.html")
                html = template.render(
                    {
                        "BASE_URL": settings.BASE_URL,
                        "nginx_addr": "http://nginx", 
                        "categories": categories,
                        "additional_logos": AdditionalLogo.objects.filter(enabled=True).all(),
                        "assessment_button": AssessmentButton.objects.last()
                    }
                )
                f.write(html.encode("utf-8"))
                f.close()

                pdf_file_path = f"{settings.MEDIA_ROOT}/exports/{export_request.uuid}.pdf"
                if os.path.exists(pdf_file_path):
                    os.unlink(pdf_file_path)

                subprocess.run(["wkhtmltopdf", "--enable-forms", f.name, pdf_file_path])

                export_request.file = f"exports/{export_request.uuid}.pdf"
                export_request.status = ExportRequest.STATUS.FINISHED
                export_request.save(update_fields=["file", "status"])
            except Exception as e:
                export_request.status = ExportRequest.STATUS.FAILED
                export_request.save(update_fields=["status"])

                logger.exception(f"Making export template for ExportRequestUUID={export_request.uuid} was failure")

                raise e

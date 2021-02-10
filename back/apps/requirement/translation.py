from modeltranslation.translator import register, TranslationOptions

from .models import Category, Requirement, TestCase


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name", "summary")
    required_languages = ("en",)


@register(Requirement)
class RequirementTranslationOptions(TranslationOptions):
    fields = ("title", "summary", "text")
    required_languages = ("en",)


@register(TestCase)
class TestCaseTranslationOptions(TranslationOptions):
    fields = ("title", "text")
    required_languages = ("en",)

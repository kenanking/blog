from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel
)
from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField
)

from home.models import HomePage

class FormField(AbstractFormField):

    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )

class ContactPage(AbstractEmailForm):

    subpage_types = []
    template = "contact/contact_page.html"

    intro = RichTextField(blank=True)
    phone = models.CharField(max_length=20, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel([
            FieldPanel("intro"),
            FieldPanel("phone", classname="col6"),
            FieldPanel("email", classname="col6"),
        ], heading="个人信息设置"),
        InlinePanel("form_fields", label="Form Fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("from_address", classname="col6"),
                FieldPanel("to_address", classname="col6"),
            ]),
            FieldPanel("subject"), 
        ], heading="邮件设置"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["page"] = HomePage.objects.all()[0]
        return context

    class Meta:
        verbose_name = verbose_name_plural = "联系信息"
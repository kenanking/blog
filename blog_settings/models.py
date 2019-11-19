from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel



@register_setting
class Blogger(BaseSetting):
    """Blogger model."""

    blogger_name = models.CharField(max_length=20, blank=False, null=False)
    blogger_intro = models.CharField(max_length=200, blank=False, null=False)
    blogger_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    facebook = models.URLField(blank=True, null=True, help_text="Facebook URL")
    twitter = models.URLField(blank=True, null=True, help_text="Twitter URL")
    github = models.URLField(blank=True, null=True, help_text="Github URL")

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("blogger_name", heading="博主"),
                FieldPanel("blogger_intro", heading="个人介绍"),
                ImageChooserPanel("blogger_image", heading="头像"),
            ], 
            heading="博主信息"
        ),
        MultiFieldPanel(
            [
                FieldPanel("facebook", heading="Facebook主页"),
                FieldPanel("twitter", heading="Twitter主页"),
                FieldPanel("github", heading="Github主页"),
            ],
            heading="社交信息"
        )
    ]

    def __str__(self):
        return self.blogger_name
    
    class Meta:
        verbose_name = "博主信息"

@register_setting
class CommentSetting(BaseSetting):
    """评论默认设置"""

    defaultpic = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        ImageChooserPanel("defaultpic", heading="默认头像"),
    ]

    class Meta:
        verbose_name = "评论设置"
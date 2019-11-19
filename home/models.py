from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from streams import blocks
from blogpost.models import BlogCategory, PostDetailPage


class HomePage(Page):
    """Home Page model."""

    templates = "home/home_page.html"
    max_count = 1

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=["bold", "italic", "h1", "h2", "h3", "h4", "h5", "h6"])
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("banner_title", heading="主页名"),
            FieldPanel("banner_subtitle", heading="副标题"),
            ImageChooserPanel("banner_image", heading="背景图"),
        ], heading="主页设置"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_posts = PostDetailPage.objects.live().public().order_by('-first_published_at')
        
        paginator = Paginator(all_posts, 6)

        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts
        context["categories"] = BlogCategory.objects.all()
        return context

    class Meta:
        verbose_name = "主页"

class AboutPage(Page):
    """About Page model."""
    subpage_types = []
    templates = "home/about_page.html"
    max_count = 1

    content = StreamField(
        [
            ("richtext", blocks.RichtextBlock()),
        ],
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=100, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("name", heading="姓名"),
        StreamFieldPanel("content", heading="介绍"),
    ]


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["page"] = HomePage.objects.all()[0]
        return context

    class Meta:
        verbose_name = "个人介绍"
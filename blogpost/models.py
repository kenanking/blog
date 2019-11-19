from django.db import models

from django import forms
from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel, 
    StreamFieldPanel, 
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import StreamField 
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.search.models import Query

from streams import blocks

class BlogAuthorOrderable(Orderable):
    """用于在写博客时选择作者"""

    page = ParentalKey("blogpost.PostDetailPage", related_name="blog_authors")
    author = models.ForeignKey(
        "blogpost.BlogAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author"),
    ]

class BlogAuthor(models.Model):
    """Blog author for snippets."""

    name = models.CharField(max_length=100)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name", heading="昵称"),
                ImageChooserPanel("image", heading="头像"),
            ], 
            heading="基本信息"
        ),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "博客作者"
        verbose_name_plural = "博客作者"

register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    """Blog category for a snippet."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text="用于定位到该目录，使用英文"
    )

    panels = [
        FieldPanel("name", heading="目录名"),
        FieldPanel("slug", heading="目录标识"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "博客目录"
        verbose_name_plural = "博客目录"
        ordering = ["name"]

register_snippet(BlogCategory)


class PostDetailPage(RoutablePageMixin, Page):
    """Parental Blog Post detail Page."""

    subpage_types = []

    template = "blogpost/blog_detail_page.html"

    custom_title = models.CharField(max_length=100, blank=False, null=False, help_text="Overwrites the default title")
    tags = ClusterTaggableManager(through="PostPageTag", blank=True)
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    categories = ParentalManyToManyField("blogpost.BlogCategory", blank=True)

    abstract = content = StreamField(
        [
            ("full_richtext", blocks.RichtextBlock()),
            ("cards", blocks.CardBlock()),
        ],
        null=True,
        blank=True,
    )

    content = StreamField(
        [
            ("full_richtext", blocks.RichtextBlock()),
            ("code_text", blocks.CodeTextBlock()),
            ("markdown_text", blocks.MarkdownTextBlock()),
            ("cards", blocks.CardBlock()),
        ],
        null=True,
        blank=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField('custom_title'),
        index.SearchField('categories'),
        index.SearchField('abstract'),
        index.SearchField('content'),

        index.RelatedFields('BlogAuthor', [
            index.SearchField('name'),
        ]),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("custom_title", heading="标题"),
        FieldPanel("tags", heading="标签"),
        ImageChooserPanel("banner_image", heading="图像（可选）"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author", min_num=1, max_num=4)
            ],
            heading="作者"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="目录"
        ),
        StreamFieldPanel("abstract", "摘要"),
        StreamFieldPanel("content", "内容"),
    ]


    class Meta:
        verbose_name = verbose_name_plural = "博客文章"


class PostPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'PostDetailPage',
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )
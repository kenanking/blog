"""Streamfields"""

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailcodeblock.blocks import CodeBlock
from wagtailmarkdown.blocks import MarkdownBlock


class RichtextBlock(blocks.RichTextBlock):
    """Richtext with all the features."""


    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "富文本编辑"

class CardBlock(blocks.StructBlock):

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=50)),
            ]
        )
    )

    class Meta:
        template = "streams/card_block.html"
        icon = "image"
        label = "图片集"

class CodeTextBlock(CodeBlock):

    class Meta:
        template = "streams/code_block.html"
        icon = "code"
        label = "代码块"

class MarkdownTextBlock(MarkdownBlock):

    class Meta:
        template = "streams/markdown_block.html"
        icon = "code"
        label = "Markdown"
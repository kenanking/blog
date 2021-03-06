# Generated by Django 2.2.6 on 2019-11-14 15:16

from django.db import migrations
import streams.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0005_auto_20191112_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postdetailpage',
            name='abstract',
            field=wagtail.core.fields.StreamField([('full_richtext', streams.blocks.RichtextBlock()), ('cards', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.core.blocks.CharBlock(max_length=50, required=True))])))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='postdetailpage',
            name='content',
            field=wagtail.core.fields.StreamField([('full_richtext', streams.blocks.RichtextBlock()), ('code_text', wagtail.core.blocks.StructBlock([('language', wagtail.core.blocks.ChoiceBlock(choices=[('bash', 'Bash/Shell'), ('batch', 'Batch'), ('c', 'C'), ('csharp', 'C#'), ('cpp', 'C++'), ('css', 'CSS'), ('diff', 'diff'), ('django', 'Django/Jinja2'), ('docker', 'Docker'), ('git', 'Git'), ('html', 'HTML'), ('ini', 'Ini'), ('javascript', 'Javascript'), ('json', 'JSON'), ('markdown', 'Markdown'), ('perl', 'Perl'), ('php', 'PHP'), ('python', 'Python'), ('scss', 'SCSS'), ('sql', 'SQL'), ('plsql', 'PL/SQL'), ('swift', 'Swift'), ('typescript', 'TypeScript'), ('yaml', 'YAML')], help_text='Coding language', identifier='language', label='Language')), ('code', wagtail.core.blocks.TextBlock(identifier='code', label='Code'))])), ('cards', wagtail.core.blocks.StructBlock([('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.core.blocks.CharBlock(max_length=50, required=True))])))]))], blank=True, null=True),
        ),
    ]

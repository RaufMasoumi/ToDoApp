from django.utils.text import slugify


def validate_title(base_title, instance, queryset):
    slug = slugify(base_title)
    matching_instance_slugs = queryset.filter(slug__startswith=slug).values_list(
        'slug', flat=True
    )
    if instance:
        matching_instance_slugs = matching_instance_slugs.exclude(pk=instance.pk)
    number = 0
    title = base_title
    while slugify(title) in matching_instance_slugs:
        number += 1
        title = f'{base_title}({number})'
    return title

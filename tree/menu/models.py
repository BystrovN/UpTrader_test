from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=30, blank=True, default='default name')
    slug = models.SlugField(unique=True)
    url = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='items',
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='child',
    )

    class Meta:
        verbose_name = 'menu item'
        verbose_name_plural = 'menu items'
        ordering = ('id',)

    def __str__(self):
        return self.slug

    def clean(self):
        if self.parent:
            if self.category != self.parent.category:
                msg = (
                    'Категория наследника должна совпадать '
                    'с категорией родителя.'
                )
                raise ValidationError(msg)

        if (
            not self.parent
            and Item.objects.filter(
                category=self.category, parent=None
            ).exists()
        ):
            msg = (
                'Необходимо указать родителя. '
                f'У меню категории {self.category} уже есть корневой элемент'
            )
            raise ValidationError(msg)

        if Item.objects.filter(slug=self.slug).exists():
            if self.id == self.parent.id:
                msg = (
                    'Элемент не может быть указан сам себе в качестве родителя'
                )
                raise ValidationError(msg)

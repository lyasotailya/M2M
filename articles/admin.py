
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_count = 0
        for form in self.forms:
            if form.cleaned_data.get("is_main", False):
                is_main_count += 1
            if is_main_count > 1:
                raise ValidationError('Основным может быть только один раздел!')
            if is_main_count == 0:
                raise ValidationError('Укажите один основной раздел')
        return super().clean()


class RelationshipInline(admin.TabularInline):
    model = Scope
    formset = RelationshipInlineFormset
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    # inlines = [RelationshipInline]


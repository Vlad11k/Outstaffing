from django.contrib import admin, messages

from mainsite.models import *


@admin.register(Blog)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_cat', 'is_published')
    ordering = ['-time_create', 'title']
    list_editable = ('is_published',)
    actions = ['set_published', 'set_draft']
    list_filter = ('is_published', 'post_cat')

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Blog.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Blog.Status.DRAFT)
        self.message_user(request, f"{count} записей сняты с публикации!", messages.WARNING)


@admin.register(Vacancies)
class VacanciesAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary', 'vacancy_cat', 'is_published')
    ordering = ['title']
    list_editable = ('is_published',)
    actions = ['set_published', 'set_draft']
    list_filter = ('is_published', 'vacancy_cat')

    @admin.action(description="Опубликовать выбранные вакансии")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Blog.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} вкансий.")

    @admin.action(description="Снять с публикации выбранные вакансии")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Blog.Status.DRAFT)
        self.message_user(request, f"{count} вакансий сняты с публикации!", messages.WARNING)


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(VacanciesCategory)
class VacanciesCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

from django import template
from django.db.models import Count

from mainsite.models import BlogCategory, VacanciesCategory

register = template.Library()


@register.inclusion_tag('mainsite/list_blog_categories.html')
def show_blog_categories(cat_selected=0):
    post_cats = BlogCategory.objects.annotate(total=Count("blog")).filter(total__gt=0)
    return {'post_cats': post_cats, 'cat_selected': cat_selected}


@register.inclusion_tag('mainsite/list_vacancy_categories.html')
def show_vacancy_categories(cat_selected=0):
    vacancy_cats = VacanciesCategory.objects.annotate(total=Count("vacancies")).filter(total__gt=0)
    return {'vacancy_cats': vacancy_cats, 'cat_selected': cat_selected}

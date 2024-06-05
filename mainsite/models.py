from django.core.validators import RegexValidator, validate_email, FileExtensionValidator
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Blog.Status.PUBLISHED)


class Blog(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='Slug')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None,
                              blank=True, null=True, verbose_name="Фото")
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Статус")
    post_cat = models.ForeignKey('BlogCategory', on_delete=models.PROTECT,
                                 related_name='blog', verbose_name="Категории")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-time_create']

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog_category', kwargs={'post_cat_slug': self.slug})


class Vacancies(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=100, verbose_name='Вакансия')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='Slug')
    salary = models.IntegerField(verbose_name='Зарплата')
    content = models.TextField()
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Статус")
    vacancy_cat = models.ForeignKey('VacanciesCategory', on_delete=models.PROTECT,
                                    related_name='vacancies', verbose_name='Направление')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('vacancy', kwargs={'vacancy_slug': self.slug})


class VacanciesCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Направление')
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('vacancies_category', kwargs={'vacancy_cat_slug': self.slug})


class UserCVs(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(max_length=100, unique=True, verbose_name='Email', validators=[validate_email])
    phone = models.CharField(max_length=100, unique=True, verbose_name='Телефон',
                             validators=[
                                 RegexValidator(
                                     regex=r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$',
                                     message='Введите действительный номер',
                                     code="invalid_registration",
                                 )
                             ])
    message = models.TextField(verbose_name='Сообщение')
    file = models.FileField(upload_to="files/%Y/%m/%d/", default=None,
                            blank=True, null=True, verbose_name="Файл",
                            validators=[FileExtensionValidator(
                                allowed_extensions=['pdf', 'docx', 'xls', 'zip', 'rar'])])

    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"

    def __str__(self):
        return self.full_name

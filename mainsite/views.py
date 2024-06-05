from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from Outstaffing import settings
from mainsite.forms import SendCvForm, SendRequest
from mainsite.models import Blog, Vacancies
from mainsite.utils import DataMixin


class HomeView(DataMixin, FormView):
    form_class = SendRequest
    template_name = 'mainsite/home.html'
    title_page = 'Главная страница'

    def get_success_url(self):
        email = self.request.POST.get('email')
        subject = 'IT-Focus'
        message = '''
        Здравствуйте, вы оставили заявку на нашем сайте.
        Хотим вас уведомить, что в ближайшее время с вами свяжется один из наших работников.
        Благодарим вас за ожидание.            
                                '''
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

        return reverse_lazy('home')


class BlogView(DataMixin, ListView):
    template_name = 'mainsite/blog.html'
    context_object_name = 'blog'
    title_page = 'Блог'
    cat_selected = 0
    paginate_by = 6

    def get_queryset(self):
        return Blog.published.all().select_related('post_cat')


class BlogCategory(DataMixin, ListView):
    template_name = 'mainsite/blog.html'
    context_object_name = 'blog'
    allow_empty = False
    paginate_by = 6

    def get_queryset(self):
        return Blog.published.filter(post_cat__slug=self.kwargs['post_cat_slug']).select_related("post_cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_cat = context['blog'][0].post_cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + post_cat.name,
                                      cat_selected=post_cat.pk,
                                      )


class ShowPost(DataMixin, DetailView):
    template_name = 'mainsite/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Blog.published, slug=self.kwargs[self.slug_url_kwarg])


class VacanciesView(DataMixin, ListView):
    template_name = 'mainsite/vacancies.html'
    context_object_name = 'vacancies'
    title_page = 'Вакансии'
    cat_selected = 0

    def get_queryset(self):
        return Vacancies.published.all().select_related('vacancy_cat')


class VacanciesCategory(DataMixin, ListView):
    template_name = 'mainsite/vacancies.html'
    context_object_name = 'vacancies'
    allow_empty = False

    def get_queryset(self):
        return Vacancies.published.filter(vacancy_cat__slug=self.
                                          kwargs['vacancy_cat_slug']).select_related("vacancy_cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy_cat = context['vacancies'][0].vacancy_cat
        return self.get_mixin_context(context,
                                      title='Направление - ' + vacancy_cat.name,
                                      cat_selected=vacancy_cat.pk,
                                      )


class ShowVacancy(DataMixin, DetailView):
    template_name = 'mainsite/vacancy.html'
    slug_url_kwarg = 'vacancy_slug'
    context_object_name = 'vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['vacancy'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Vacancies.published, slug=self.kwargs[self.slug_url_kwarg])


class SendingView(DataMixin, CreateView):
    form_class = SendCvForm
    template_name = 'mainsite/sendCV.html'
    title_page = 'Отправить резюме'

    def get_success_url(self):
        return reverse_lazy('home')

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Outstaffing import settings
from mainsite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('blog/<slug:post_cat_slug>/', views.BlogCategory.as_view(), name='blog_category'),

    path('vacancies/', views.VacanciesView.as_view(), name='vacancies'),
    path('vacancy/<slug:vacancy_slug>/', views.ShowVacancy.as_view(), name='vacancy'),
    path('vacancies/<slug:vacancy_cat_slug>/', views.VacanciesCategory.as_view(), name='vacancies_category'),

    path('sending', views.SendingView.as_view(), name='sending'),

    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
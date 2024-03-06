from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from blog.forms import BlogForm
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Blog
from main.models import Mail, Client


def is_contentmanager(user):
    """Возвращает булево значение на вхождение пользователя в группу."""
    return user.groups.filter(name='Контент-менеджер').exists()


class MainListView(ListView):
    """отображениe главной"""
    model = Blog
    template_name = 'blog/main.html'
    extra_context = {'title': 'OWL-mail'}

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)[:2]

        return queryset

    def get_context_data(self, *args, **kwargs):
        """Получает контекстные данных для страницы."""
        context_data = super().get_context_data(*args, **kwargs)
        context_data['mail_count'] = Mail.objects.all().count()
        context_data['mail_active'] = Mail.objects.filter(status='RUNING').count()
        context_data['mail_client'] = Client.objects.all().count()

        return context_data


class BlogListView(ListView):
    """Просмотр списка блогов"""
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    """просмотр блога отдельно"""
    model = Blog

    def get_object(self, queryset=None):
        """счётчик просмотров"""
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    """создание блога"""
    model = Blog
    fields = ('title', 'content', 'preview', 'is_published')
    success_url = reverse_lazy('blog:blog_list')

    def has_permission(self):
        user = self.request.user
        return is_contentmanager(user) or user.is_superuser

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogDeleteView(DeleteView):
    """удалиение блога"""
    model = Blog
    success_url = reverse_lazy('blog:blog_list')

    def has_permission(self):
        user = self.request.user
        return is_contentmanager(user) or user.is_superuser


class BlogUpdateView(UpdateView):
    """редактирование записи"""
    model = Blog
    fields = ('title', 'content', 'preview', 'is_published')

    def has_permission(self):
        user = self.request.user
        return is_contentmanager(user) or user.is_superuser

    def get_success_url(self):
        """перенаправление на старицу редактируемого объекта после конформации"""
        return reverse_lazy('blog:view_blog', args=[self.kwargs.get("pk")])

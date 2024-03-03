from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.views.generic import (ListView, CreateView, DetailView, UpdateView,
                                  DeleteView)
from django.urls import reverse_lazy
from main.forms import MailForm, MessageForm, ClientForm, ManagerForm
from main.models import Mail, Message, Client, Logs


def is_manager(user):
    """Возвращает булево значение на вхождение пользователя в группу."""
    return user.groups.filter(name='Менеджер').exists()


# Mail


class MailListView(LoginRequiredMixin, ListView):
    """отображениe всех рассылок."""
    model = Mail
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status__in=('COMPLETE', 'RUNING'))
        return queryset


class MailEndingListView(LoginRequiredMixin, ListView):
    """отображениe всех рассылок."""
    model = Mail
    template_name = 'main/mail_list_complete.html'

    def get_queryset(self):
        """
        Возвращает список товаров по номеру категории и
        статусу публикации для отображения на странице.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(status='COMPLETE')

        return queryset


class MailCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """созданиe новой рассылки."""
    model = Mail
    form_class = MailForm
    permission_required = ('mail.add_mail',)
    success_url = reverse_lazy('main:mail_list')

    def has_permission(self):
        """ проверкa разрешений."""
        perms = self.get_permission_required()
        user = self.request.user
        return user.has_perms(perms)

    def form_valid(self, form):
        """Валидация формы создания товара и версий."""
        if form.is_valid():
            new_mail = form.save()
            new_mail.creator = self.request.user
            new_mail.save()

        return super().form_valid(form)


class MailUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для изменения определенной рассылки."""
    model = Mail
    form_class = MailForm
    permission_required = ('mail.set_status',)
    success_url = reverse_lazy('main:mail_list')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        perms = self.get_permission_required()
        mail = self.get_object()
        user = self.request.user
        return user == mail.creator or user.has_perms(perms)

    def get_form_class(self):
        """Возвращает форму в зависимости от роли пользователя."""
        user = self.request.user
        mail = self.get_object()

        if is_manager(user):
            return ManagerForm
        elif user.is_superuser or user == mail.creator:
            return MailForm


class MailDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """отображениe 1 рассылки."""
    model = Mail
    permission_required = ('mail.view_mailing',)

    def has_permission(self):
        perms = self.get_permission_required()
        mail = self.get_object()
        user = self.request.user
        return user == mail.creator or user.has_perms(perms)


class MailDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """удалениe рассылки."""
    model = Mail
    permission_required = ('mail.delete_mailing',)
    success_url = reverse_lazy('main:mailing_list')

    def has_permission(self):
        perms = self.get_permission_required()
        mail = self.get_object()
        user = self.request.user
        return user == mail.creator or user.has_perms(perms)


# MailingMessage


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """создание сообщения."""
    model = Message
    form_class = MessageForm
    permission_required = ('mail.add_message',)
    success_url = reverse_lazy('main:mailing_create')

    def has_permission(self):
        user = self.request.user
        return not is_manager(user)


# Client


class ClientListView(LoginRequiredMixin, ListView):
    """Класс для отображения всех рассылок."""
    model = Client


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """создание нового получателя."""
    model = Client
    form_class = ClientForm
    permission_required = ('mail.add_client',)
    success_url = reverse_lazy('main:mail_create')

    def has_permission(self):
        user = self.request.user
        return not is_manager(user)


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """удалениt рассылки"""
    model = Client
    permission_required = ('mail.delete_client',)
    success_url = reverse_lazy('main:mailing_list')

    def has_permission(self):
        """Настраивает способ проверки разрешений."""
        perms = self.get_permission_required()
        client = self.get_object()
        user = self.request.user
        return user == client.creator or user.has_perms(perms)
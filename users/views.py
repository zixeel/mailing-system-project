from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404

from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, ListView
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
# from main.views import is_manager

from config import settings
from users.forms import UserRegisterForm
from users.models import User


class RegisterView(CreateView):
    """Регистрация"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verify')

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_active = False
        new_user.save()
        token = get_random_string(32)
        verification_url = reverse('users:verification', args=[token])
        new_user.token = token
        send_mail(
            subject='Подтверждение почты Сервиса рассылок "СИБИРСКАЯ ОСПА"',
            message=f'Пожалуйста, перейдите по ссылке для подтверждения почты: '
                    f'{settings.HOST}{verification_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class VerificationView(TemplateView):
    template_name = 'users/verification.html'


class EmailVerify(View):
    def get(self, request, *args, **kwargs):
        user_token = self.kwargs.get('token')
        our_token = User.objects.filter(token=user_token).first()
        print(our_token)
        new_user = User.objects.filter(email=our_token).first()
        print(new_user)

        if our_token:
            new_user.is_active = True
            new_user.save()
            return redirect('users:login')
        else:
            return redirect('users:verify_error')


class ProfileView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    permission_required = ('users.set_is_active',)
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def has_permission(self):

        perms = self.get_permission_required()
        user = self.request.user

        return user == self.get_object() or user.has_perms(perms)

    # def get_form_class(self):
    #     user = self.request.user
    #
    #     if is_manager(user):
    #         return ManagerForm
    #     elif user.is_superuser or user == self.get_object():
    #         return UserProfileForm


class UserListView(LoginRequiredMixin, ListView):
    model = User


@permission_required('users.set_is_active')
def set_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()
    return redirect('users:users')

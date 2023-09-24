import random
from django.contrib.auth.decorators import permission_required, login_required
from django import forms
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.core.mail import send_mail
from users.models import User
from users.forms import UserRegisterForm, UserForm
from django.views.generic import ListView
from django.shortcuts import redirect, get_object_or_404


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Вход в систему',
    }


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject='Поздравляем с регистрацией!',
            message='Вы зарегистрировались на нашей платформе.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class Profileview(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    extra_context = {
        'title': 'Мой профиль',
    }

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(ListView):
    model = User
    template_name = 'user_list.html'  # Замените на имя вашего шаблона
    context_object_name = 'users'  # Имя переменной контекста для передачи списка пользователей в шаблон
    extra_context = {
        'title': 'Список пользователей',
    }

    def get_queryset(self):
        return User.objects.all()


def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    user.is_blocked = True
    user.save()

    return redirect('users:user_list')


def unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    user.is_blocked = False
    user.save()

    return redirect('users:user_list')


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])

    send_mail(
        subject='Вы сменили пароль!',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('newsletter:index'))



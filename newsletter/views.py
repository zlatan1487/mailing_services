from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView
from newsletter.models import Customer, Mailing, MailText, MailingLog
from django.urls import reverse_lazy, reverse
from newsletter.mailing_forms import MailingForm, MailTextForm, CustomerForm
from django.forms import inlineformset_factory, modelformset_factory
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Permission
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from random import sample
from blog.models import Blog


class mailingCreateView(CreateView):
    """
        Класс для создания новой рассылки.
    """

    model = Mailing
    template_name = 'newsletter/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('newsletter:index')

    extra_context = {
        'title': 'Создать рассылку',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        CustomerFormset = modelformset_factory(MailText, form=MailTextForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = CustomerFormset(self.request.POST)
        else:
            context_data['formset'] = CustomerFormset(queryset=Customer.objects.none())

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        form.instance.creator = self.request.user

        self.object = form.save()

        if formset.is_valid():
            for customer_form in formset:
                if customer_form.cleaned_data:
                    customer = customer_form.save(commit=False)
                    customer.mailing_list = self.object
                    customer.save()

        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = self.request.user.customer_set.all()
        return form


class mailingListView(ListView):
    """
    Класс для просмотра списка рассылок.
    """
    template_name = 'newsletter/index.html'
    context_object_name = 'newsletter_list'

    extra_context = {
        'title': 'Список рассылок',
    }

    @method_decorator(login_required(login_url=reverse_lazy('users:login')), name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_blocked:
            logout(request)
            return render(request, 'users/blocked_user.html')  # Вызываем шаблон
        else:
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Mailing.objects.all()
        else:
            return Mailing.objects.filter(creator_id=self.request.user.id).select_related('message', 'creator').prefetch_related('clients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        unique_customers = set()

        if current_user.is_staff:
            all_users = get_user_model().objects.all()

            for user in all_users:
                newsletter_customers = Customer.objects.filter(user=user)
                for newsletter_customer in newsletter_customers:
                    unique_customers.add(newsletter_customer.email)
        else:
            newsletter_customers = Customer.objects.filter(user=current_user)

            for newsletter_customer in newsletter_customers:
                unique_customers.add(newsletter_customer.email)

        total_unique_customers = len(unique_customers)

        context['total_unique_customers'] = total_unique_customers

        # Добавляем подсчет активных рассылок
        if current_user.is_staff:
            # Если пользователь - админ, показываем все активные рассылки
            active_mailings_count = Mailing.objects.filter(status='started').count()
        else:
            # Если пользователь не админ, показываем только активные рассылки, созданные им
            active_mailings_count = Mailing.objects.filter(status='started', creator=current_user).count()

        context['active_mailings_count'] = active_mailings_count

        # Получаем случайные блоги
        if current_user.is_staff:
            # Если пользователь - суперпользователь, показываем три случайных блога всех пользователей
            random_blogs = Blog.objects.order_by('?')[:3]
        else:
            # Если пользователь не суперпользователь, показываем три случайных своих блога
            random_blogs = Blog.objects.filter(author=current_user).order_by('?')[:3]

        context['random_blogs'] = random_blogs

        return context


class mailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm

    success_url = reverse_lazy('newsletter:index')

    extra_context = {
        'title': 'Создать рассылку',
    }


class mailingDetailView(DeleteView):
    model = Mailing
    template_name = 'newsletter/mailing_detail.html'
    ontext_object_name = 'newsletter_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message_topic'] = self.object.message.topic  # Добавляем message_topic в контекст
        context['title'] = self.object.message.topic  # Задаем значение title
        return context


class mailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('newsletter:index')


class MailingLogListView(ListView):
    model = MailingLog
    template_name = 'newsletter/mailing_logs.html'  # Создайте шаблон для отображения списка логов
    context_object_name = 'mailing_logs'  # Имя переменной контекста в шаблоне
    extra_context = {
        'title': 'Логи рассылки',
    }


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'newsletter/create_customer.html'
    success_url = reverse_lazy('newsletter:customer_list')
    extra_context = {
        'title': 'Создать клиента',
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CustomerListView(ListView):
    model = Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers'

    extra_context = {
        'title': 'Список клиентов',
    }

    def get_queryset(self):
        if self.request.user.is_staff:
            return Customer.objects.all()
        else:
            return Customer.objects.filter(user=self.request.user)



def send_mailing(request, mailing_id):
    mailing = Mailing.objects.get(pk=mailing_id)

    clients = mailing.clients.all()

    message_text = mailing.message.message

    mailing_logs = []

    for client in clients:
        subject = mailing.message.topic
        from_email = 'vitalik.karpukhin@list.ru'
        recipient_list = [client.email]

        try:
            send_mail(subject, message_text, from_email, recipient_list)
            status = 'success'
            server_response = 'Письмо успешно отправлено'
        except Exception as e:
            status = 'failure'
            server_response = str(e)

        mailing_log = MailingLog(mailing=mailing, status=status, server_response=server_response)
        mailing_logs.append(mailing_log)

    MailingLog.objects.bulk_create(mailing_logs)

    mailing.status = 'completed'
    mailing.save()
    return HttpResponse("Рассылка успешно отправлена")





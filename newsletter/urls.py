from django.urls import path
from newsletter.views import mailingListView,                             \
                            mailingDetailView, \
                            mailingUpdateView, \
                            mailingDeleteView, \
                            mailingCreateView, \
                            send_mailing, \
                            CustomerCreateView, \
                            CustomerListView, \
                            MailingLogListView
app_name = 'newsletter'  # Пространство имен для приложения "newsletter"

urlpatterns = [
    path('', mailingListView.as_view(), name='index'),
    path('newsletter/<int:pk>/', mailingDetailView.as_view(), name='mailing_detail'),
    path('create/', mailingCreateView.as_view(), name='mailing_create'),
    path('edit/<int:pk>/', mailingUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>', mailingDeleteView.as_view(), name='mailing_delete'),
    path('send_mailing/<int:mailing_id>/', send_mailing, name='send_mailing'),
    path('create_customer/', CustomerCreateView.as_view(), name='create_customer'),
    path('customer_list/', CustomerListView.as_view(), name='customer_list'),
    path('mailing_logs/', MailingLogListView.as_view(), name='mailing_log_list'),
]


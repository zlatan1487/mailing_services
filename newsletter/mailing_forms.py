from django import forms
from newsletter.models import Mailing, MailText, Customer


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    # Добавляем поле message из модели MailText
    message_topic = forms.CharField(
        max_length=100,
        label='Тема рассылки',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    message_text = forms.CharField(
        label='Текст сообщения',
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Mailing
        fields = ['frequency', 'status', 'clients']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если форма редактирования, устанавливаем начальные значения для полей message
        if self.instance and self.instance.message:
            self.initial['message_topic'] = self.instance.message.topic
            self.initial['message_text'] = self.instance.message.message  # Исправлено здесь

    def clean(self):
        cleaned_data = super().clean()
        # Получаем значения полей message_topic и message_text из формы
        message_topic = cleaned_data.get('message_topic')
        message_text = cleaned_data.get('message_text')

        # Проверяем, что оба поля заполнены
        if message_topic and message_text:
            # Если форма валидна, создаем или обновляем объект MailText
            mail_text, created = MailText.objects.update_or_create(
                topic=message_topic,
                defaults={'message': message_text}  # Исправлено здесь
            )
            # Присваиваем созданный или существующий объект MailText полю message
            self.instance.message = mail_text

        return cleaned_data


class MailTextForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailText
        fields = '__all__'


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name', 'middle_name']


# class MailingForm(StyleFormMixin, forms.ModelForm):
#     # Остальной код формы остается без изменений
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)  # Извлекаем текущего пользователя из kwargs
#         super().__init__(*args, **kwargs)
#         # Ограничиваем выбор клиентов текущего пользователя
#         if user:
#             self.fields['clients'].queryset = user.customer_set.all()

from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'preview_image',)
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        # Получаем текущего пользователя и устанавливаем его как автора блога
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/list.html'
    context_object_name = 'Ваши блоги'
    extra_context = {
        'title': context_object_name,
    }

    def get_queryset(self):
        if self.request.user.is_superuser:
            # Если пользователь администратор, покажем все блоги
            queryset = Blog.objects.filter(is_published=True)
        else:
            # Иначе покажем только блоги текущего пользователя
            current_user = self.request.user
            queryset = Blog.objects.filter(author=current_user, is_published=True)

        return queryset


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'preview_image',)

    def get_success_url(self):
        # Получаем идентификатор успешно обновленного продукта
        product_id = self.object.pk

        # Используем функцию reverse_lazy для создания URL с указанным id
        success_url = reverse_lazy('blog:view', kwargs={'pk': product_id})
        return success_url


class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'О блоге'
    extra_context = {
        'title': context_object_name,
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')

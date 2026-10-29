"""
Контроллеры приложения blog (только CBV).

- BlogPostListView: список статей. Через get_queryset выводятся только
  опубликованные (is_published=True).
- BlogPostDetailView: страница статьи. Через get_object при каждом
  открытии увеличивается счётчик просмотров. Доп. задание: когда статья
  набирает ровно 100 просмотров, на свою почту отправляется письмо
  с поздравлением.
- BlogPostCreateView: создание статьи.
- BlogPostUpdateView: редактирование; после успешного сохранения
  пользователь перенаправляется на страницу этой статьи (success_url).
- BlogPostDeleteView: удаление с подтверждением.
"""

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from blog.forms import BlogPostForm
from blog.models import BlogPost

VIEWS_MILESTONE = 100


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Блог"
        return context


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        post = super().get_object(queryset)

        # F() увеличивает счётчик на стороне БД — так два одновременных
        # открытия не «потеряют» просмотр.
        BlogPost.objects.filter(pk=post.pk).update(views_count=F("views_count") + 1)
        post.refresh_from_db(fields=["views_count"])

        if post.views_count == VIEWS_MILESTONE:
            self.send_milestone_email(post)

        return post

    @staticmethod
    def send_milestone_email(post):
        """Доп. задание: письмо себе, когда статья набрала 100 просмотров."""
        recipient = settings.BLOG_NOTIFY_EMAIL
        if not recipient:
            return
        send_mail(
            subject=f"Статья «{post.title}» набрала {VIEWS_MILESTONE} просмотров!",
            message=(
                f"Поздравляем! Статья «{post.title}» только что набрала "
                f"{VIEWS_MILESTONE} просмотров."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=True,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context


class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"

    def get_success_url(self):
        return reverse("blog:blogpost_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новая статья"
        return context


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"

    def get_success_url(self):
        # После редактирования — на страницу этой же статьи.
        return reverse("blog:blogpost_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование статьи"
        return context


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    context_object_name = "post"
    success_url = reverse_lazy("blog:blogpost_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление статьи"
        return context

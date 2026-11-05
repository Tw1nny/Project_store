"""
Команда создаёт группы пользователей и назначает им права:

- «Модератор продуктов»: снимать товары с публикации
  (catalog.can_unpublish_product) и удалять любые товары
  (catalog.delete_product);
- «Контент-менеджер» (доп. задание): управлять статьями блога
  (blog.add/change/delete/view_blogpost).

Команду можно запускать повторно: группы не дублируются, а их права
приводятся к списку ниже.

    python manage.py create_groups

Пользователя добавляют в группу в админке: Пользователи → нужный
пользователь → поле «Группы».
"""

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError

MODERATOR_GROUP = "Модератор продуктов"
CONTENT_MANAGER_GROUP = "Контент-менеджер"

GROUP_PERMISSIONS = {
    MODERATOR_GROUP: [
        "catalog.can_unpublish_product",
        "catalog.delete_product",
    ],
    CONTENT_MANAGER_GROUP: [
        "blog.add_blogpost",
        "blog.change_blogpost",
        "blog.delete_blogpost",
        "blog.view_blogpost",
    ],
}


class Command(BaseCommand):
    help = "Создаёт группы «Модератор продуктов» и «Контент-менеджер» с нужными правами"

    def handle(self, *args, **options):
        for group_name, permission_names in GROUP_PERMISSIONS.items():
            permissions = [self.get_permission(name) for name in permission_names]

            group, created = Group.objects.get_or_create(name=group_name)
            group.permissions.set(permissions)

            status = "создана" if created else "обновлена"
            self.stdout.write(self.style.SUCCESS(f"Группа «{group_name}» {status}:"))
            for name in permission_names:
                self.stdout.write(f"  - {name}")

    @staticmethod
    def get_permission(full_name):
        app_label, codename = full_name.split(".")
        try:
            return Permission.objects.get(content_type__app_label=app_label, codename=codename)
        except Permission.DoesNotExist:
            raise CommandError(
                f"Право {full_name} не найдено. Сначала примените миграции: python manage.py migrate"
            )

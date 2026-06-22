from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Category(models.Model):
    title = models.CharField(verbose_name='Наименование', max_length=255)
    description = models.TextField(verbose_name='Описание')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Supplier(models.Model):
    title = models.CharField(verbose_name='Наименование', max_length=255)
    fio = models.CharField(verbose_name='ФИО руководителя', max_length=255)
    phone = models.CharField(verbose_name='Телефон', max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"


class Unit(models.Model):
    title = models.CharField(verbose_name='Наименование', max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"


class ProductGroup(models.Model):
    title = models.CharField(verbose_name='Наименование', max_length=255)
    description = models.TextField(verbose_name='Описание')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Группа товаров"
        verbose_name_plural = "Группы товаров"


class Product(models.Model):
    title = models.CharField(verbose_name='Наименование', max_length=255)
    group = models.ForeignKey(to=ProductGroup, verbose_name="Группа", on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Campaign(models.Model):
    title = models.CharField(verbose_name='Наименование', max_length=255)
    start_at = models.DateField(verbose_name='Дата начала')
    end_at = models.DateField(verbose_name='Дата окончания')
    product = models.ForeignKey(to=Product, verbose_name="Товар", on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Описание')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"


class ExportCategory(models.Model):
    title = models.CharField(verbose_name='Наименование', max_length=255)
    description = models.TextField(verbose_name='Описание')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Категория вывоза"
        verbose_name_plural = "Категории вывоза"


class ClientCategory(models.Model):
    title = models.CharField(verbose_name='Наименование', max_length=255)
    description = models.TextField(verbose_name='Описание')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Категория клиентов"
        verbose_name_plural = "Категории клиентов"


class Client(models.Model):
    title = models.CharField(verbose_name='Наименование', max_length=255)
    fio = models.CharField(verbose_name='ФИО руководителя', max_length=255)
    phone = models.CharField(verbose_name='Телефон', max_length=255)
    category = models.ForeignKey(to=ClientCategory, verbose_name="Категория", on_delete=models.CASCADE)
    email = models.EmailField(verbose_name='Электронная почта')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Deal(models.Model):
    date = models.DateField(verbose_name='Дата')
    product = models.ForeignKey(to=Product, verbose_name="Товар", on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, verbose_name="Клиент", on_delete=models.CASCADE)
    count = models.PositiveIntegerField(verbose_name='Количество')
    export_category = models.ForeignKey(
        to=ExportCategory, verbose_name="Категория вывоза", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.client.title} — {self.product.title} × {self.count}"

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"


class Interaction(models.Model):
    INTERACTION_TYPES = [
        ('feedback', 'Обратная связь'),
        ('ticket', 'Тикет'),
        ('proposal', 'Предложение'),
    ]
    STATUS_CHOICES = [
        ('open', 'Открыт'),
        ('closed', 'Закрыт'),
    ]

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    type = models.CharField(verbose_name='Тип', max_length=10, choices=INTERACTION_TYPES)
    title = models.CharField(verbose_name='Тема', max_length=255)
    description = models.TextField(verbose_name='Описание')
    status = models.CharField(
        verbose_name='Статус', max_length=10, choices=STATUS_CHOICES, default='open'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self) -> str:
        return f"{self.get_type_display()} — {self.title}"

    class Meta:
        verbose_name = "Взаимодействие"
        verbose_name_plural = "Взаимодействия"
        ordering = ['-created_at']


class Notification(models.Model):
    date = models.DateField(verbose_name='Дата', default=date.today)
    text = models.CharField(verbose_name='Текст', max_length=255)
    user = models.ForeignKey(to=User, verbose_name="Пользователь", on_delete=models.CASCADE)
    is_hidden = models.BooleanField(verbose_name="Скрыто?", default=False)

    def __str__(self) -> str:
        return f"{self.user} — {self.text}"

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ['-date']

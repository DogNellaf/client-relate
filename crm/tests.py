from datetime import date

from django.test import TestCase, Client as TestClient
from django.urls import reverse
from django.contrib.auth.models import User

from crm.models import (
    Category,
    Supplier,
    Unit,
    ProductGroup,
    Product,
    Campaign,
    ExportCategory,
    ClientCategory,
    Client,
    Deal,
    Interaction,
    Notification,
)
from crm.forms import InteractionForm, CustomUserCreationForm, CustomAuthenticationForm


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------

class CategoryModelTest(TestCase):
    def test_str(self):
        cat = Category(title='Электроника', description='Электронные товары')
        self.assertEqual(str(cat), 'Электроника')

    def test_meta(self):
        self.assertEqual(Category._meta.verbose_name, 'Категория')
        self.assertEqual(Category._meta.verbose_name_plural, 'Категории')


class SupplierModelTest(TestCase):
    def test_str(self):
        sup = Supplier(title='ООО Поставщик', fio='Иванов И.И.', phone='+7-999-000-00-00')
        self.assertEqual(str(sup), 'ООО Поставщик')

    def test_meta(self):
        self.assertEqual(Supplier._meta.verbose_name, 'Поставщик')


class UnitModelTest(TestCase):
    def test_str(self):
        unit = Unit(title='кг')
        self.assertEqual(str(unit), 'кг')


class ProductGroupModelTest(TestCase):
    def test_str(self):
        pg = ProductGroup(title='Напитки', description='Все виды напитков')
        self.assertEqual(str(pg), 'Напитки')


class ProductModelTest(TestCase):
    def setUp(self):
        self.group = ProductGroup.objects.create(title='Группа', description='Описание')

    def test_str(self):
        product = Product.objects.create(title='Товар А', group=self.group, price='100.50')
        self.assertEqual(str(product), 'Товар А')

    def test_price_decimal(self):
        product = Product.objects.create(title='Товар Б', group=self.group, price='9999.99')
        product.refresh_from_db()
        self.assertAlmostEqual(float(product.price), 9999.99, places=2)


class CampaignModelTest(TestCase):
    def setUp(self):
        group = ProductGroup.objects.create(title='Г', description='Д')
        self.product = Product.objects.create(title='Товар', group=group, price='10.00')

    def test_str(self):
        campaign = Campaign.objects.create(
            title='Летняя акция',
            start_at=date(2024, 6, 1),
            end_at=date(2024, 8, 31),
            product=self.product,
            description='Описание акции',
        )
        self.assertEqual(str(campaign), 'Летняя акция')


class ExportCategoryModelTest(TestCase):
    def test_str(self):
        ec = ExportCategory(title='Опт', description='Оптовые поставки')
        self.assertEqual(str(ec), 'Опт')


class ClientCategoryModelTest(TestCase):
    def test_str(self):
        cc = ClientCategory(title='VIP', description='Важные клиенты')
        self.assertEqual(str(cc), 'VIP')


class ClientModelTest(TestCase):
    def setUp(self):
        self.category = ClientCategory.objects.create(title='Стандарт', description='Обычные клиенты')

    def test_str(self):
        client = Client.objects.create(
            title='ООО Клиент',
            fio='Петров П.П.',
            phone='+7-888-000-00-00',
            category=self.category,
            email='client@example.com',
        )
        self.assertEqual(str(client), 'ООО Клиент')


class DealModelTest(TestCase):
    def setUp(self):
        group = ProductGroup.objects.create(title='Г', description='Д')
        self.product = Product.objects.create(title='Продукт', group=group, price='50.00')
        cat = ClientCategory.objects.create(title='Кат', description='Д')
        self.client_obj = Client.objects.create(
            title='Клиент', fio='Ф', phone='1', category=cat, email='a@b.com'
        )
        self.export_cat = ExportCategory.objects.create(title='Экспорт', description='Д')

    def test_str(self):
        deal = Deal.objects.create(
            date=date(2024, 1, 15),
            product=self.product,
            client=self.client_obj,
            count=5,
            export_category=self.export_cat,
        )
        self.assertIn('Клиент', str(deal))
        self.assertIn('Продукт', str(deal))

    def test_count_positive(self):
        deal = Deal.objects.create(
            date=date(2024, 1, 15),
            product=self.product,
            client=self.client_obj,
            count=10,
            export_category=self.export_cat,
        )
        self.assertEqual(deal.count, 10)


class InteractionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_str_feedback(self):
        obj = Interaction.objects.create(
            user=self.user, type='feedback', title='Проблема', description='Описание'
        )
        self.assertIn('Проблема', str(obj))

    def test_str_ticket(self):
        obj = Interaction.objects.create(
            user=self.user, type='ticket', title='Тикет 1', description='Описание'
        )
        self.assertIn('Тикет 1', str(obj))

    def test_default_status_open(self):
        obj = Interaction.objects.create(
            user=self.user, type='proposal', title='Идея', description='Подробности'
        )
        self.assertEqual(obj.status, 'open')

    def test_created_at_auto(self):
        obj = Interaction.objects.create(
            user=self.user, type='feedback', title='Т', description='Д'
        )
        self.assertIsNotNone(obj.created_at)

    def test_ordering_newest_first(self):
        from django.utils import timezone
        import datetime
        obj1 = Interaction.objects.create(
            user=self.user, type='feedback', title='Первый', description='Д'
        )
        obj2 = Interaction.objects.create(
            user=self.user, type='ticket', title='Второй', description='Д'
        )
        # Force obj2 to have a strictly later timestamp
        Interaction.objects.filter(pk=obj2.pk).update(
            created_at=timezone.now() + datetime.timedelta(seconds=1)
        )
        qs = list(Interaction.objects.all())
        self.assertEqual(qs[0].pk, obj2.pk)


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='notifuser', password='pass123')

    def test_str(self):
        n = Notification.objects.create(user=self.user, text='Привет!')
        self.assertIn('notifuser', str(n))
        self.assertIn('Привет!', str(n))

    def test_default_is_hidden_false(self):
        n = Notification.objects.create(user=self.user, text='Текст')
        self.assertFalse(n.is_hidden)

    def test_default_date_today(self):
        n = Notification.objects.create(user=self.user, text='Текст')
        self.assertEqual(n.date, date.today())

    def test_hide(self):
        n = Notification.objects.create(user=self.user, text='Текст')
        n.is_hidden = True
        n.save()
        n.refresh_from_db()
        self.assertTrue(n.is_hidden)


# ---------------------------------------------------------------------------
# Form tests
# ---------------------------------------------------------------------------

class InteractionFormTest(TestCase):
    def test_valid_form_with_set_type(self):
        form = InteractionForm(data={
            'title': 'Тема', 'description': 'Описание', 'type': '', 'status': 'open'
        })
        form.set_type('feedback')
        self.assertTrue(form.is_valid(), form.errors)

    def test_set_type_overrides_value(self):
        form = InteractionForm(data={
            'title': 'Т', 'description': 'Д', 'type': 'ticket', 'status': 'open'
        })
        form.set_type('proposal')
        form.is_valid()
        self.assertEqual(form.cleaned_data['type'], 'proposal')

    def test_missing_title_invalid(self):
        form = InteractionForm(data={
            'title': '', 'description': 'Описание', 'type': 'feedback', 'status': 'open'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_missing_description_invalid(self):
        form = InteractionForm(data={
            'title': 'Тема', 'description': '', 'type': 'ticket', 'status': 'open'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_form_controls_class(self):
        form = InteractionForm()
        self.assertIn('form-control', form.fields['title'].widget.attrs.get('class', ''))
        self.assertIn('form-control', form.fields['description'].widget.attrs.get('class', ''))


class CustomUserCreationFormTest(TestCase):
    def get_valid_data(self):
        return {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }

    def test_valid_form(self):
        form = CustomUserCreationForm(data=self.get_valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_email_saved(self):
        form = CustomUserCreationForm(data=self.get_valid_data())
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, 'new@example.com')

    def test_password_mismatch_invalid(self):
        data = self.get_valid_data()
        data['password2'] = 'DifferentPass!'
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        data = self.get_valid_data()
        data['email'] = 'not-an-email'
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class CustomAuthenticationFormTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='authuser', password='pass123word!')

    def test_valid_credentials(self):
        form = CustomAuthenticationForm(data={'username': 'authuser', 'password': 'pass123word!'})
        self.assertTrue(form.is_valid(), form.errors)

    def test_wrong_password(self):
        form = CustomAuthenticationForm(data={'username': 'authuser', 'password': 'wrongpass'})
        self.assertFalse(form.is_valid())

    def test_form_control_class_applied(self):
        form = CustomAuthenticationForm()
        for field in form.fields.values():
            self.assertIn('form-control', field.widget.attrs.get('class', ''))


# ---------------------------------------------------------------------------
# View tests
# ---------------------------------------------------------------------------

class HomeViewTest(TestCase):
    def setUp(self):
        self.client_http = TestClient()
        self.user = User.objects.create_user(username='homeuser', password='pass123!')

    def test_redirect_unauthenticated(self):
        resp = self.client_http.get(reverse('home'))
        self.assertRedirects(resp, f"{reverse('login')}?next={reverse('home')}")

    def test_home_authenticated(self):
        self.client_http.login(username='homeuser', password='pass123!')
        resp = self.client_http.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html')


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client_http = TestClient()

    def test_get_register(self):
        resp = self.client_http.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'register.html')

    def test_post_register_creates_user(self):
        resp = self.client_http.post(reverse('register'), {
            'username': 'reguser',
            'email': 'reg@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertRedirects(resp, reverse('home'))
        self.assertTrue(User.objects.filter(username='reguser').exists())

    def test_authenticated_user_redirected(self):
        User.objects.create_user(username='existing', password='pass123!')
        self.client_http.login(username='existing', password='pass123!')
        resp = self.client_http.get(reverse('register'))
        self.assertRedirects(resp, reverse('home'))

    def test_invalid_registration(self):
        resp = self.client_http.post(reverse('register'), {
            'username': '',
            'email': 'bad',
            'password1': '123',
            'password2': '456',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(User.objects.filter(email='bad').exists())


class LoginViewTest(TestCase):
    def setUp(self):
        self.client_http = TestClient()
        User.objects.create_user(username='loginuser', password='pass123!')

    def test_get_login(self):
        resp = self.client_http.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'login.html')

    def test_post_login_success(self):
        resp = self.client_http.post(reverse('login'), {
            'username': 'loginuser', 'password': 'pass123!'
        })
        self.assertRedirects(resp, reverse('home'))

    def test_post_login_failure(self):
        resp = self.client_http.post(reverse('login'), {
            'username': 'loginuser', 'password': 'wrongpass'
        })
        self.assertEqual(resp.status_code, 200)

    def test_authenticated_user_redirected(self):
        self.client_http.login(username='loginuser', password='pass123!')
        resp = self.client_http.get(reverse('login'))
        self.assertRedirects(resp, reverse('home'))


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client_http = TestClient()
        self.user = User.objects.create_user(username='logoutuser', password='pass123!')

    def test_logout_post(self):
        self.client_http.login(username='logoutuser', password='pass123!')
        resp = self.client_http.post(reverse('logout'))
        self.assertRedirects(resp, reverse('login'))

    def test_logout_get_redirects(self):
        resp = self.client_http.get(reverse('logout'))
        self.assertRedirects(resp, reverse('login'))


class FeedbackCreateViewTest(TestCase):
    def setUp(self):
        self.client_http = TestClient()
        self.user = User.objects.create_user(username='fbuser', password='pass123!')

    def test_redirect_unauthenticated(self):
        resp = self.client_http.get(reverse('feedback_create'))
        self.assertEqual(resp.status_code, 302)

    def test_get_form(self):
        self.client_http.login(username='fbuser', password='pass123!')
        resp = self.client_http.get(reverse('feedback_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'interaction_form.html')

    def test_post_creates_interaction(self):
        self.client_http.login(username='fbuser', password='pass123!')
        resp = self.client_http.post(reverse('feedback_create'), {
            'title': 'Тема обратной связи',
            'description': 'Подробное описание',
            'status': 'open',
        })
        self.assertRedirects(resp, reverse('home'))
        obj = Interaction.objects.get(user=self.user)
        self.assertEqual(obj.type, 'feedback')
        self.assertEqual(obj.title, 'Тема обратной связи')

    def test_post_invalid_no_title(self):
        self.client_http.login(username='fbuser', password='pass123!')
        resp = self.client_http.post(reverse('feedback_create'), {
            'title': '',
            'description': 'Описание',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Interaction.objects.filter(user=self.user).exists())


class TicketCreateViewTest(TestCase):
    def setUp(self):
        self.client_http = TestClient()
        self.user = User.objects.create_user(username='tickuser', password='pass123!')

    def test_post_creates_ticket(self):
        self.client_http.login(username='tickuser', password='pass123!')
        resp = self.client_http.post(reverse('ticket_create'), {
            'title': 'Тикет проблема',
            'description': 'Описание проблемы',
            'status': 'open',
        })
        self.assertRedirects(resp, reverse('home'))
        obj = Interaction.objects.get(user=self.user)
        self.assertEqual(obj.type, 'ticket')


class OfferCreateViewTest(TestCase):
    def setUp(self):
        self.client_http = TestClient()
        self.user = User.objects.create_user(username='offeruser', password='pass123!')

    def test_post_creates_offer(self):
        self.client_http.login(username='offeruser', password='pass123!')
        resp = self.client_http.post(reverse('offer_create'), {
            'title': 'Предложение',
            'description': 'Хорошая идея',
            'status': 'open',
        })
        self.assertRedirects(resp, reverse('home'))
        obj = Interaction.objects.get(user=self.user)
        self.assertEqual(obj.type, 'proposal')


class MyInteractionsViewTest(TestCase):
    def setUp(self):
        self.client_http = TestClient()
        self.user = User.objects.create_user(username='myuser', password='pass123!')
        self.other = User.objects.create_user(username='otheruser', password='pass123!')
        Interaction.objects.create(user=self.user, type='feedback', title='Моё', description='Д')
        Interaction.objects.create(user=self.other, type='ticket', title='Чужое', description='Д')

    def test_redirect_unauthenticated(self):
        resp = self.client_http.get(reverse('my_interactions'))
        self.assertEqual(resp.status_code, 302)

    def test_shows_only_own_interactions(self):
        self.client_http.login(username='myuser', password='pass123!')
        resp = self.client_http.get(reverse('my_interactions'))
        self.assertEqual(resp.status_code, 200)
        items = list(resp.context['page_obj'].object_list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].title, 'Моё')

    def test_filter_by_type(self):
        Interaction.objects.create(user=self.user, type='ticket', title='Тикет мой', description='Д')
        self.client_http.login(username='myuser', password='pass123!')
        resp = self.client_http.get(reverse('my_interactions') + '?type=ticket')
        items = list(resp.context['page_obj'].object_list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].type, 'ticket')


class NotificationsViewTest(TestCase):
    def setUp(self):
        self.client_http = TestClient()
        self.user = User.objects.create_user(username='notifuser2', password='pass123!')
        self.other = User.objects.create_user(username='othernotif', password='pass123!')
        Notification.objects.create(user=self.user, text='Моё уведомление')
        Notification.objects.create(user=self.other, text='Чужое уведомление')

    def test_redirect_unauthenticated(self):
        resp = self.client_http.get(reverse('notifications'))
        self.assertEqual(resp.status_code, 302)

    def test_shows_only_own_notifications(self):
        self.client_http.login(username='notifuser2', password='pass123!')
        resp = self.client_http.get(reverse('notifications'))
        self.assertEqual(resp.status_code, 200)
        items = list(resp.context['page_obj'].object_list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].text, 'Моё уведомление')

    def test_hidden_notifications_not_shown(self):
        Notification.objects.filter(user=self.user).update(is_hidden=True)
        self.client_http.login(username='notifuser2', password='pass123!')
        resp = self.client_http.get(reverse('notifications'))
        items = list(resp.context['page_obj'].object_list)
        self.assertEqual(len(items), 0)


class HideNotificationViewTest(TestCase):
    def setUp(self):
        self.client_http = TestClient()
        self.user = User.objects.create_user(username='hideuser', password='pass123!')
        self.other = User.objects.create_user(username='hideother', password='pass123!')
        self.own_notif = Notification.objects.create(user=self.user, text='Моё')
        self.other_notif = Notification.objects.create(user=self.other, text='Чужое')

    def test_redirect_unauthenticated(self):
        resp = self.client_http.post(reverse('hide_notification'), {'id': self.own_notif.pk})
        self.assertEqual(resp.status_code, 302)

    def test_hide_own_notification(self):
        self.client_http.login(username='hideuser', password='pass123!')
        resp = self.client_http.post(reverse('hide_notification'), {'id': self.own_notif.pk})
        self.assertRedirects(resp, reverse('notifications'))
        self.own_notif.refresh_from_db()
        self.assertTrue(self.own_notif.is_hidden)

    def test_cannot_hide_other_users_notification(self):
        self.client_http.login(username='hideuser', password='pass123!')
        resp = self.client_http.post(reverse('hide_notification'), {'id': self.other_notif.pk})
        self.assertEqual(resp.status_code, 403)
        self.other_notif.refresh_from_db()
        self.assertFalse(self.other_notif.is_hidden)

    def test_get_request_redirects(self):
        self.client_http.login(username='hideuser', password='pass123!')
        resp = self.client_http.get(reverse('hide_notification'))
        self.assertRedirects(resp, reverse('notifications'))

    def test_invalid_id_returns_404(self):
        self.client_http.login(username='hideuser', password='pass123!')
        resp = self.client_http.post(reverse('hide_notification'), {'id': 99999})
        self.assertEqual(resp.status_code, 404)

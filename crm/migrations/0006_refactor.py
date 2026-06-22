import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20240605_1238'),
    ]

    operations = [
        # Fix Suplier → Supplier
        migrations.RenameModel(
            old_name='Suplier',
            new_name='Supplier',
        ),

        # Fix Notification.date default (was frozen datetime at migration time)
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата'),
        ),

        # Fix Notification.user verbose_name
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                to='auth.user',
                verbose_name='Пользователь',
            ),
        ),

        # Fix Product.price: FloatField → DecimalField
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(
                verbose_name='Стоимость', max_digits=12, decimal_places=2
            ),
        ),

        # Fix Deal.count: IntegerField → PositiveIntegerField
        migrations.AlterField(
            model_name='deal',
            name='count',
            field=models.PositiveIntegerField(verbose_name='Количество'),
        ),

        # Fix Interaction.status: remove null/blank, reduce max_length
        migrations.AlterField(
            model_name='interaction',
            name='status',
            field=models.CharField(
                verbose_name='Статус',
                max_length=10,
                choices=[('open', 'Открыт'), ('closed', 'Закрыт')],
                default='open',
            ),
        ),

        # Add ordering to Interaction
        migrations.AlterModelOptions(
            name='interaction',
            options={
                'verbose_name': 'Взаимодействие',
                'verbose_name_plural': 'Взаимодействия',
                'ordering': ['-created_at'],
            },
        ),

        # Add ordering to Notification
        migrations.AlterModelOptions(
            name='notification',
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
                'ordering': ['-date'],
            },
        ),
    ]

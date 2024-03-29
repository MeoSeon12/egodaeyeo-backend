# Generated by Django 4.0.6 on 2022-07-22 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('item', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('대여 종료', '대여 종료'), ('대여 가능', '대여 가능'), ('예약 중', '예약 중'), ('대여 중', '대여 중')], max_length=10, verbose_name='상태')),
                ('start_date', models.DateTimeField(verbose_name='시작일')),
                ('end_date', models.DateTimeField(verbose_name='반납일')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'contracts',
            },
        ),
        migrations.CreateModel(
            name='ContractHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contract.contract')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'contract_histories',
            },
        ),
    ]

# Generated by Django 4.0.2 on 2022-03-05 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('splitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('reason', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expense_Total',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_amount', models.IntegerField()),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_total_receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_total_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Group_Friend', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('creater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Creater', to=settings.AUTH_USER_MODEL)),
                ('friends', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Settle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_debt', to='splitter.expense')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_debts', to='splitter.group')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='final_transactions',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='final_transactions',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='personal_expense',
            name='user',
        ),
        migrations.RemoveField(
            model_name='personal_income',
            name='user',
        ),
        migrations.RemoveField(
            model_name='room',
            name='creater',
        ),
        migrations.RemoveField(
            model_name='room',
            name='members',
        ),
        migrations.AlterUniqueTogether(
            name='room_members',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='room_members',
            name='member',
        ),
        migrations.RemoveField(
            model_name='room_members',
            name='room',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='payer',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='room',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='splitters',
        ),
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='debt',
        ),
        migrations.DeleteModel(
            name='final_transactions',
        ),
        migrations.DeleteModel(
            name='Personal_expense',
        ),
        migrations.DeleteModel(
            name='Personal_income',
        ),
        migrations.DeleteModel(
            name='room',
        ),
        migrations.DeleteModel(
            name='room_members',
        ),
        migrations.DeleteModel(
            name='transaction',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='friend',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Group_name', to='splitter.group'),
        ),
        migrations.AddField(
            model_name='expense',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_expense', to='splitter.group'),
        ),
        migrations.AddField(
            model_name='expense',
            name='payer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_payer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='expense',
            name='splitters',
            field=models.ManyToManyField(related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='friend',
            unique_together={('group', 'friend')},
        ),
    ]
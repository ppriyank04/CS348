# Generated by Django 4.2.11 on 2024-03-31 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('total_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('daily_profit_loss', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10, unique=True)),
                ('company_name', models.CharField(max_length=200)),
                ('stock_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price_bought_at', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.stock')),
            ],
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]

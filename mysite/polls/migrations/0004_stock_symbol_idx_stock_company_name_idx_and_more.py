# Generated by Django 4.2.11 on 2024-04-28 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_delete_portfoliosummary_stock_price_stock_quantity_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='stock',
            index=models.Index(fields=['symbol'], name='symbol_idx'),
        ),
        migrations.AddIndex(
            model_name='stock',
            index=models.Index(fields=['company_name'], name='company_name_idx'),
        ),
        migrations.AddIndex(
            model_name='stock',
            index=models.Index(fields=['symbol', 'company_name'], name='symbol_company_name_idx'),
        ),
    ]

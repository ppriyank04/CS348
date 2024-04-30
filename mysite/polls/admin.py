from django.contrib import admin
from django.db import transaction
from .models import Stock
from django.db import connection
from django.urls import path
from .views import stock_report  # Import the stock_report function from views.py



class StockAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'company_name', 'stock_type', 'quantity', 'price']
    search_fields = ['symbol', 'company_name']  # Enable a search bar for symbol and company_name fields
    

    @admin.action(description='Perform a raw SQL query')
    def perform_raw_sql_query(self, request, queryset):
        with transaction.atomic():
            for stock in queryset:
                # Assuming you want to perform an UPDATE as an example
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE polls_stock SET quantity = %s WHERE id = %s",
                        [stock.quantity, stock.id]
                    )
                    # If you were retrieving data, you would use cursor.fetchone() or cursor.fetchall()

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        # Overridden save_model method to include raw SQL with transaction.
        super().save_model(request, obj, form, change)
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE polls_stock SET quantity = %s WHERE id = %s",
                [obj.quantity, obj.id]
            )
            # No fetch required since this is an update query.

    @transaction.atomic
    def delete_model(self, request, obj):
        # Overridden delete_model method to include raw SQL with transaction.
        super().delete_model(request, obj)
        with connection.cursor() as cursor:
            # Assuming there's some cleanup needed in another table related to stock
            cursor.execute(
                "DELETE FROM related_table WHERE stock_id = %s",
                [obj.id]
            )
            # No fetch required since this is a delete query.

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('report/', self.admin_site.admin_view(self.report_view))
        ]
        return custom_urls + urls

    def report_view(self, request):
        # The actual view function is in views.py, redirect to it
        return stock_report(request)


admin.site.register(Stock, StockAdmin)

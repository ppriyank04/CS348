from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from .models import Stock
from .forms import StockReportForm
from django.db import connection
from .forms import StockReportForm


def main_page(request):
    stocks = Stock.objects.all()
    return render(request, 'polls/main_page.html', {'stocks': stocks})

# Adding a new stock entry using the ORM
@transaction.atomic
def add_stock(request):
    if request.method == 'POST':
        try:
            symbol = request.POST.get('symbol')
            company_name = request.POST.get('company_name')
            stock_type = request.POST.get('stock_type')
            quantity = int(request.POST.get('quantity'))
            price = float(request.POST.get('price'))
            
            new_stock = Stock(symbol=symbol, company_name=company_name, 
                              stock_type=stock_type, quantity=quantity, price=price)
            new_stock.save()
            messages.success(request, "Stock added successfully.")
            return redirect('polls:main_page')  # Redirect to the same page after adding
        except ValueError:
            # Handle the case where int or float conversion fails
            messages.error(request, "There was an error with your input.")
        except Exception as e:
            # Handle other possible exceptions
            messages.error(request, f"Error adding stock: {str(e)}")
            
    # If GET request or if there's an error, render the page with the form
    return render(request, 'polls/add_stock.html')

# Update stock information with concurrency control
@transaction.atomic
def update_stock(request):
    stock_id = request.GET.get('stock_id')
    if stock_id is None:
        # Handle the case where stock_id is not provided in the query parameters
        messages.error(request, "Stock ID is required.")
        return redirect('polls:main_page')  # Redirect to main_page or any other appropriate page
        
    stock = get_object_or_404(Stock.objects.select_for_update(), pk=stock_id)
    
    if request.method == 'POST':
        # Update stock attributes based on the form data
        stock.symbol = request.POST.get('symbol')
        stock.company_name = request.POST.get('company_name')
        stock.stock_type = request.POST.get('stock_type')
        stock.quantity = request.POST.get('quantity')
        stock.price = request.POST.get('price')
        stock.save()
        messages.success(request, "Stock updated successfully.")
        return redirect('polls:main_page')  # Redirect to the add_stock page after updating
    
    return render(request, 'polls/update_stock.html', {'stock': stock})

def sell_stock(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        quantity_to_sell = int(request.POST.get('quantity'))

        # Retrieve the stock based on the symbol
        stock = get_object_or_404(Stock, symbol=symbol)

        # Check if the quantity to sell is greater than 0
        if quantity_to_sell <= 0:
            messages.error(request, "Quantity to sell must be greater than 0.")
            return redirect('polls:sell_stock')

        # Check if the quantity to sell is less than or equal to the available quantity
        if quantity_to_sell > stock.quantity:
            messages.error(request, f"Not enough quantity available to sell. Available quantity: {stock.quantity}")
            return redirect('polls:sell_stock')

        # If the entire quantity is sold, delete the stock entry
        if quantity_to_sell == stock.quantity:
            stock.delete()
        else:
            # Update the stock quantity and save the changes
            stock.quantity -= quantity_to_sell
            stock.save()

        messages.success(request, f"{quantity_to_sell} units of {symbol} sold successfully.")
        return redirect('polls:main_page')
    else:
        return render(request, 'polls/sell_stock.html')
    
# Complex reporting using ORM and aggregate functions
def stock_report(request):
    form = StockReportForm(request.GET or None)
    if request.method == 'GET' and form.is_valid():
        start_price = form.cleaned_data.get('start_price')
        end_price = form.cleaned_data.get('end_price')
        stock_type = form.cleaned_data.get('stock_type')

        # Define SQL query with placeholders for parameters
        query = """
            SELECT AVG(price) AS avg_price, AVG(quantity) AS avg_quantity
            FROM polls_stock
            WHERE (%s IS NULL OR price >= %s)
            AND (%s IS NULL OR price <= %s)
            AND (%s IS NULL OR stock_type = %s)
        """

        # Execute the prepared statement with parameters
        with connection.cursor() as cursor:
            cursor.execute(query, [start_price, start_price, end_price, end_price, stock_type, stock_type])
            row = cursor.fetchone()

        # Extract average price and quantity from the result
        average_price = row[0] or 0
        average_quantity = row[1] or 0

        # Get filtered stocks based on form data
        stocks = Stock.objects.filter(price__gte=start_price, price__lte=end_price)
        if stock_type:
            stocks = stocks.filter(stock_type=stock_type)

    else:
        stocks = Stock.objects.none()
        average_price = 0
        average_quantity = 0

    context = {
        'form': form,
        'stocks': stocks,
        'average_price': average_price,
        'average_quantity': average_quantity,
    }
    return render(request, 'polls/stock_report.html', context)
import random

# Data arrays
symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', 'TSLA']
company_names = ['Apple Inc.', 'Google LLC', 'Microsoft Corp.', 'Amazon.com, Inc.', 'Facebook, Inc.', 'Tesla, Inc.']
stock_types = ['dividend', 'growth', 'value', 'other']

# Generate 50 SQL INSERT statements
sql_statements = []
for i in range(50):
    symbol = random.choice(symbols)
    company_name = random.choice(company_names)
    stock_type = random.choice(stock_types)
    quantity = random.randint(1, 10000)
    price = round(random.uniform(10.0, 1000.0), 2)

    sql = f"INSERT INTO public.polls_stock (symbol, company_name, stock_type, quantity, price) VALUES ('{symbol}', '{company_name}', '{stock_type}', {quantity}, {price});"
    sql_statements.append(sql)

# Printing out the SQL statements
for statement in sql_statements:
    print(statement)

import pandas as pd

# Para cada cidade, calcular:
    # Total de clientes
    # Total de pedidos
    # Ticket médio por pedido
# Identificar os 3 produtos mais vendidos em termos de quantidade.
# Calcular a receita mensal (agrupando por mês/ano do campo order_date).
# Listar os clientes que nunca fizeram um pedido.
# Use pd.cut para criar faixas de idade:
    # 18–25
    # 26–35
    # 36–45
    # 46–60
    # 60+
# Calcule, para cada faixa etária:
# Número de clientes
# Gasto médio total por cliente

def segregate_into_age(df):
    print('==== Segragating into age range ====')
    bins=[18,25,35,45,60,float('inf')]
    labels=['18-25', '26-35', '36-45', '46-60', '60+']
    df['age_range'] = pd.cut(df['age'], bins=bins, labels=labels)
    resume = df.groupby('age_range', observed=False).agg(
        total_clients=('customer_id', pd.Series.nunique),
        mean_spent=('total_amount', 'mean')
    )
    print(resume)
    return

def calculate_by_city(df_o, df_oi, df_c):
    print('==== Total Clients by City ====')
    total_clients_city = df_c.groupby('city')['customer_id'].size()
    print(total_clients_city)
    print('==== Total Orders by City ====')
    df_oc = pd.merge(df_o, df_c, on='customer_id', how='inner')
    total_order_city = df_oc.groupby('city')['order_id'].size()
    print(total_order_city)
    print('==== Average ticket by city ====')
    df_oic = pd.merge(pd.merge(df_o, df_oi, on='order_id', how='inner'), df_c, left_on='customer_id', right_on='customer_id', how='inner')
    mean_ticket_city = df_oic.groupby('city').agg(
        mean_ticket=('price', 'mean')
    )
    print(mean_ticket_city)
    return

def identify_products_by_quantity(df_oi):
    print('==== Best products by quantity ====')
    resume = df_oi.groupby('product_name').agg(
        quantity_sold=('quantity', 'sum')
    )
    resume = resume.sort_values('quantity_sold', ascending=False)
    print(resume.iloc[:3])
    return

def calculate_month_revenue(df):
    print('==== Monthly revenue ====')
    df['order_date'] = pd.to_datetime(df['order_date'])
    resume = df.groupby([df['order_date'].dt.year, df['order_date'].dt.month], observed=False)['total_amount'].sum().unstack(fill_value=0)
    print(resume.head(13))
    return

def clients_never_order(df):
    print('==== Client never ordered ====')
    resume = df.groupby('customer_id').agg(
        customer_name=('name', 'max'),
        total_order=('order_id', 'count')
    )
    print(f'The customer: {resume[resume["total_order"] <= 0].iloc[0, 0]} never did a purchase')
    return 

def main ():
    df_orders = pd.read_csv('./data/orders.csv')
    df_order_items = pd.read_csv('./data/order_items.csv')
    df_customers = pd.read_csv('./data/customers.csv')
    merged = pd.merge(pd.merge(df_orders, df_order_items, left_on='order_id', right_on='order_id', how='inner'), df_customers, on='customer_id', how='right')
    
    print('==== TASK 1 ====')
    calculate_by_city(df_orders, df_order_items, df_customers)
    identify_products_by_quantity(df_order_items)
    calculate_month_revenue(df_orders)
    clients_never_order(pd.merge(df_customers, df_orders, on='customer_id', how='left'))
    segregate_into_age(merged)
    return

if __name__ == '__main__':
    main()
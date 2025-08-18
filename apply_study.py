import pandas as pd

# 1. Preparação dos Dados
# Carregue os três arquivos CSV (vendas.csv, vendedores.csv, produtos.csv).
# Limpeza: A coluna valor_venda no vendas.csv tem valores ausentes. Substitua esses valores pela mediana da coluna.
# Consolidação: Mescle os três DataFrames em um único DataFrame chamado df_completo.

# 2. Cálculo de Bônus com apply()
# Defina uma função: Crie uma função Python chamada calcula_bonus que recebe uma única linha do DataFrame como entrada. A função deve conter a seguinte lógica:
# Se o valor_venda for maior que R$ 5.000, o bônus base é 10% do valor da venda.
# Caso contrário, o bônus base é 5% do valor da venda.
# O bônus final de cada transação é o bônus base multiplicado pelo fator_performance do produto.
# Aplique a função: Use o método df_completo.apply(calcula_bonus, axis=1) para criar uma nova coluna chamada bonus_transacao, que conterá o bônus calculado para cada venda.

# 3. Relatório Final
# Agrupe o df_completo por nome_vendedor.
# Calcule o bonus_total (a soma de todos os bônus das transações) e o valor_total_vendas para cada vendedor.
# Classifique o resultado pelo bonus_total em ordem decrescente.
# Imprima o relatório final para identificar os vendedores de melhor performance.

def calcula_bonus(row):
    base_bonus = 0
    if row['sell_value'] >= 5000:
        base_bonus = (row['sell_value'] * 0.10) * row['performance_factor'] 
        return base_bonus
    base_bonus = (row['sell_value'] * 0.05) * row['performance_factor']
    return base_bonus
    

def main():
    print('==== TASK 1 ====')
    df_sells = pd.read_csv('./data/sells.csv')
    df_sellers = pd.read_csv('./data/sellers.csv')
    df_products = pd.read_csv('./data/products_v2.csv')
    
    df_sells['sell_value'] = df_sells['sell_value'].fillna(df_sells['sell_value'].median())
    complete_df = pd.merge(pd.merge(df_sells, df_products, left_on='product_id', right_on='id', how='left'), df_sellers, left_on='seller_id', right_on='id', how='left')
    complete_df = complete_df.drop(columns=['id_x', 'id_y'])
    print(complete_df.head())

    print('\n==== TASK 2 ====')
    complete_df['transaction_bonus'] = complete_df.apply(lambda row: round(calcula_bonus(row), 2), axis=1)
    print(complete_df)

    print('\n==== TASK 3 ====')
    report = complete_df.groupby('seller_id', observed=False).agg(
        seller_name=('seller_name', 'max'),
        total_sell_value=('sell_value', 'sum'),
        total_bonus=('transaction_bonus', 'sum'),
        branch=('branch', 'max')
    ).sort_values('total_sell_value', ascending=False)
    print(report)
    return

if __name__ == '__main__':
    main()
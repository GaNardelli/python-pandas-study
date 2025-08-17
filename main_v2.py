import pandas as pd

def main():
    df_sells = pd.read_csv('./data/sells.csv')
    df_sellers = pd.read_csv('./data/sellers.csv')
    df_products = pd.read_csv('./data/products.csv')

    print("===== TASK 1 =====")
    df_sells = df_sells.fillna(value=df_sells['sell_value'].mean())
    print(df_sells.head(3))

    print("\n===== TASK 2 =====")
    merge_sells_products = pd.merge(df_sells, df_products, left_on='product_id', right_on='id', how='left').drop('id', axis=1)
    merge_complete = pd.merge(merge_sells_products, df_sellers, left_on='seller_id', right_on='id', how='left').drop('id', axis=1)
    print(merge_complete.head(11))

    print("\n===== TASK 3 =====")
    bins = [0,1000,5000,10000, float('inf')]
    labels = ["Low", "Medium", "High", "Very High"]
    merge_complete['sell_magin'] = pd.cut(merge_complete['sell_value'], bins=bins, labels=labels)
    print(merge_complete.head(11))

    print("\n===== TASK 4 =====")
    group_by_branch_margin = merge_complete.groupby(['branch', 'sell_magin'], observed=False).size().unstack(fill_value=0)
    total_branch_margin = group_by_branch_margin.sum(axis=1)
    percentage_branch_margin = (group_by_branch_margin.div(total_branch_margin, axis=0) * 100).round(2)
    print(percentage_branch_margin)

    print("\n===== TASK 5 =====")
    best_seller_df = merge_complete.groupby('seller_id').agg(
        seller_name=('seller_name', 'max'),
        total_sell_value=('sell_value', 'sum'),
    ).sort_values('total_sell_value', ascending=False)
    best_seller = best_seller_df['seller_name'].iloc[0]
    print(f'The best seller is: {best_seller}')

    best_product_df = merge_complete.groupby('product_id').agg(
        product_name=('product_name', 'max'),
        total_sell_value=('sell_value', 'sum'),
    ).sort_values('total_sell_value', ascending=False)
    best_product = best_product_df['product_name'].iloc[0]
    print(f'The best product is: {best_product}')
    return

if __name__ == '__main__':
    main()
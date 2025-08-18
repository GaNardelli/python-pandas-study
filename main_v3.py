import pandas as pd

# 1. Data Preparation and Cleaning
# Load Data: Load the three CSV files (sells.csv, sellers.csv, products.csv) into separate pandas DataFrames. (OK)
#
# Handle Missing Data: The sell_value column in sells.csv has some missing values (NaN). 
# Fill these missing values with the median of the sell_value column instead of the mean. 
# Using the median is a more robust approach as it's less affected by extreme outliers.
#
# Consolidate Data: Merge the three DataFrames into a single DataFrame, df_complete, containing all relevant information for each transaction.


# 2. Performance Metrics and Conditional Logic
# Calculate Total Team Sales: For each branch, calculate the total value of all sales.
# 
# Categorize Branches: Create a new column in your DataFrame called branch_performance.
# Categorize each branch's performance as High if its total sales exceed $20,000, and Standard otherwise.
# 
# Calculate Individual Bonus: Calculate a bonus for each salesperson based on two criteria:
# Base Bonus: A salesperson receives a base bonus of 5% of their total sales.
# Team Performance Bonus: If a salesperson's branch_performance is High, they receive an additional 2% bonus on their total sales.

# 3. Final Reporting
#
# Create a final summary DataFrame showing each seller_name, their total_sales, and their final calculated bonus.
# Sort this summary DataFrame in descending order by bonus and print the result.

def categorize_calculate_bonus(df):
    total_team_sales_by_branch = df.groupby('branch').agg(
        total_sales_value=('sell_value', 'sum')
    )
    bins = [0, 20000, float('inf')]
    labels = ['Standard', 'High']
    total_team_sales_by_branch['branch_performance'] = pd.cut(total_team_sales_by_branch['total_sales_value'], bins=bins, labels=labels)
    print(total_team_sales_by_branch)
    salesmen_total = df.groupby('seller_id').agg(
        seller_id=('seller_id', 'max'),
        seller_name=('seller_name', 'max'),
        total_sales_seller=('sell_value', 'sum'),
        branch=('branch', 'max'),
    )
    # its important to merge then because we are going to use this at the lambda function
    salesmen_total = pd.merge(salesmen_total, total_team_sales_by_branch, on='branch', how='left')
    salesmen_total['base_bonus'] = (salesmen_total['total_sales_seller']*0.05).round(2)
    # REMEMBER THE AXIS, DEFAULT IS TO CHANGE THE COLUMN NO THE ROW
    salesmen_total['team_bonus'] = salesmen_total.apply(lambda row: (row['total_sales_seller']*0.02).round(2) if row['branch_performance'] == 'High' else 0, axis=1)
    # what if i wanto to create the column with the bonus add together?
    salesmen_total['total_bonus'] = salesmen_total['team_bonus'] + salesmen_total['base_bonus'] # Simple actually
    print(salesmen_total)
    return salesmen_total

def main():
    print("===== TASK 1 =====")
    df_sells = pd.read_csv('./data/sells.csv')
    df_products = pd.read_csv('./data/products.csv')
    df_sellers = pd.read_csv('./data/sellers.csv')

    df_sells = df_sells.fillna(df_sells['sell_value'].median())
    
    merge_sells_products = pd.merge(df_sells, df_products, left_on='product_id', right_on='id', how='left')
    complete_merge = pd.merge(merge_sells_products, df_sellers, left_on='seller_id', right_on='id', how='left')

    print(complete_merge.head(4))

    print("\n===== TASK 2 =====")
    calculated_bonus = categorize_calculate_bonus(complete_merge)

    print("\n===== TASK 3 =====")
    print(calculated_bonus.sort_values('total_bonus', ascending=True))
    return

if __name__ == '__main__':
    main()
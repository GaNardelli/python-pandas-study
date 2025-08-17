import pandas as pd

# Task 1 – Client Segmentation
# Categorize clients into risk groups (Low, Fair, Good, Excellent) based on risk_score.
# Low (300–579)
# Fair (580–669)
# Good (670–739)
# Excellent (740–850)
# Count the number of clients in each group.

# Task 2 – Premium Analysis by State and Product
# Compute total premium and average premium for each state and product.
# Identify which state + product combination has the highest average premium.

# Task 3 – Claims Analysis
# Compute total claims per client.
# Identify clients who never made a claim.

# Task 4 – High-Risk Premium Exposure
# List clients with risk_score < 600 who have more than 1 policy.
# Show their name, number of policies, total premium.

# Task 5 – Income vs Premium
# Calculate for each client: total_premium / income ratio.
# List the top 3 clients who spend the largest proportion of their income on premiums.

# Task 6 – Claims by Month
# Create a monthly report of total claims (sum) and number of claims.
# Identify the month with the highest claims.

# Task 7: For each state, calculate the percentage of policies that are AUTO vs HOME.

# Task 8: Identify customers whose total claim amounts exceed their total premiums.

def client_segmentation(df):
    print("====== TASK 1 ======")
    bins = [299, 579, 669, 739, 850]
    labels = ['Low', 'Fair', 'Good', 'Excellent']
    df['risk_score_label'] = pd.cut(df['risk_score'], bins=bins, labels=labels)
    number_risk_label = df.groupby('risk_score_label', observed=False).agg(
        risk_label_count=('risk_score_label', 'count'),
        risk_score=('risk_score', 'max')
    )
    print(number_risk_label)
    return

def __return_mean_total_premium(df):
    return df.agg(
        total_premium=('premium', 'sum'),
        mean_premium=('premium', 'mean')
    )

def premium_state_product(df):
    print("\n====== TASK 2 ======")
    total_mean_state = __return_mean_total_premium(df.groupby('state'))
    print("====== STATE ======")
    print(total_mean_state)
    total_mean_product = __return_mean_total_premium(df.groupby('product'))
    print("\n====== PRODUCT ======")
    print(total_mean_product)
    return

def claim_analysis(df):
    print("\n====== TASK 3 ======")
    total_claims_per_client = df.groupby('customer_id').agg(
        total_claims=('claim_amount', 'count')
    )
    print("\n====== Total Claim ======")
    print(total_claims_per_client)
    print("\n====== Never Claim ======")
    print(total_claims_per_client.query('total_claims <= 0'))
    return

def high_risk_premium_exposure(df):
    print("\n====== TASK 4 ======")
    list_clients = df.groupby('customer_id').agg(
        customer_id=('customer_id', 'first'),
        policy_count=('policy_id', 'count'),
        max_risk_score=('risk_score', 'max'),
        client_name=('name', 'first'),
        total_premium=('premium', 'sum')
    ).query('policy_count > 1 and max_risk_score < 600')
    print(list_clients)
    return

def income_vs_premium(df):
    print("\n====== TASK 5 ======")
    premium_income_ratio = df.groupby('customer_id').agg(
        customer_id=('customer_id', 'first'),
        total_premium=('premium','sum'),
        income=('income', 'max')
    )
    premium_income_ratio['premium_income_ratio'] = premium_income_ratio['income']/premium_income_ratio['total_premium']
    premium_income_ratio = premium_income_ratio.sort_values('premium_income_ratio', ascending=False)
    print(premium_income_ratio.head(3))
    return 

def calims_by_month(df):
    print("\n====== TASK 6 ======")
    df['claim_date'] = pd.to_datetime(df['claim_date'])
    month_group = df.groupby(df['claim_date'].dt.month).agg(
        total_claims=('claim_amount', 'count'),
        total_claims_value=('claim_amount', 'sum')
    )
    month_group = month_group.sort_values('total_claims', ascending=False)
    print(month_group.head(3))
    print(f'Month with highest number of claims: {month_group.index[0]}')
    return

def percentage_products_state(df):
    print("\n====== TASK 7 ======")
    # Task 7: For each state, calculate the percentage of policies that are AUTO vs HOME.
    group_state_product = df.groupby(['state', 'product']).size().unstack(fill_value=0)
    print(group_state_product)
    total_policies_states = group_state_product.sum(axis=1)
    print(total_policies_states)
    policy_percentages = (group_state_product.div(total_policies_states, axis=0) * 100).round(2)
    print(policy_percentages)
    return

def main():
    df_policy = pd.read_csv('./data/policies.csv')
    df_claims = pd.read_csv('./data/claims.csv')
    df_clients = pd.read_csv('./data/clients.csv')

    client_segmentation(df_clients)

    premium_state_product(df_policy)

    merge_policy_claims = pd.merge(df_policy, df_claims, on='policy_id', how='left')
    merge_policy_claims_clients = pd.merge(merge_policy_claims, df_clients, left_on='customer_id', right_on='id', how='inner')
    claim_analysis(merge_policy_claims_clients)

    merge_policy_clients = pd.merge(df_policy, df_clients, left_on='customer_id', right_on='id', how='inner')
    high_risk_premium_exposure(merge_policy_clients)

    income_vs_premium(merge_policy_clients)

    calims_by_month(merge_policy_claims_clients)

    percentage_products_state(merge_policy_claims)
    return

if __name__ == '__main__':
    main()
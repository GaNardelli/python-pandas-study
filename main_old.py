import pandas as pd
import numpy as np

# Low (300–579)
# Fair (580–669)
# Good (670–739)
# Excellent (740–850)

def define_customer_by_risk(clients, policies, claims):
    bins = [299, 579, 669, 739, 850]
    labels = ['Low', 'Fair', 'Good', 'Excellent']
    clients['risk_group'] = pd.cut(clients['risk_score'], bins=bins, labels=labels)
    
    merged_pc = pd.merge(policies, claims, on='policy_id', how="left")

    merged = pd.merge(merged_pc, clients, left_on='customer_id', right_on='id', how='inner')

    calculate_mean_avg = merged.groupby('risk_group', observed=False).agg(
        avg_premium=('premium', 'mean'),
        avg_claim=('claim_amount', 'mean')
    )
    print(calculate_mean_avg)

def calculate_by_state(df):
    df_calculate = df.groupby('state').agg(
        total_premium=('premium', 'sum'),
        total_claims=('claim_amount', 'sum'),
    )
    df_calculate['loss_ratio'] = df_calculate['total_claims']/df_calculate['total_premium']
    print(df_calculate)

def high_risk_clients(df):
    more_than_two_claims = df[df['risk_score'] < 600].groupby('customer_id').agg(
        name=('name','first'),
        risk_score=('risk_score', 'first'),
        number_of_claims=('claim_id', 'count'),
        total_premium=('premium', 'sum')
    ).query('number_of_claims > 2')
    print(more_than_two_claims.head())

def income_vs_premium_affordability(df):
    premium_to_income = df.groupby('customer_id').agg(
        sum_policy=('premium', 'sum'),
        income=('income', 'first'),
        customer_id=('customer_id', 'first')
    )
    premium_to_income['premium_to_income_ratio'] = premium_to_income['sum_policy']/premium_to_income['income']
    print(premium_to_income)

def main():
    df_policies = pd.read_csv('./data/policies.csv')
    df_claims = pd.read_csv('./data/claims.csv')
    df_clients = pd.read_csv('./data/clients.csv')
    
    print("====== TASK 2 =======")
    define_customer_by_risk(df_clients, df_policies, df_claims)

    print("\n====== TASK 3 =======")
    merged_pclaims = pd.merge(df_policies, df_claims, left_on='policy_id', right_on='policy_id', how="left")
    calculate_by_state(merged_pclaims)

    print("\n====== TASK 4 =======")
    merged_pcclients = pd.merge(merged_pclaims, df_clients, left_on='customer_id', right_on='id', how='inner')
    high_risk_clients(merged_pcclients)

    print("\n====== TASK 5 =======")
    merged_pclients = pd.merge(df_policies, df_clients, left_on='customer_id', right_on='id', how='inner')
    income_vs_premium_affordability(merged_pclients)


if __name__ == '__main__':
    main()
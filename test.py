import pandas as pd

def main():
    dfp = pd.read_csv('./data/policies.csv')
    dfp_group = dfp.groupby(['state', 'product'])
    print(dfp_group.head())
    print(dfp_group.size())
    dfp_group = dfp_group.size().unstack(fill_value=0)
    print(dfp_group)
    total_policies = dfp_group.sum(axis=1)
    print(total_policies)
    percentage = (dfp_group.div(total_policies, axis=0) * 100).round(2)
    print(percentage)
    return

if __name__ == '__main__':
    main()
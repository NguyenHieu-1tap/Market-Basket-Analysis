import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules


def csv_output(a):
    a.to_csv('output.csv', index=False)


# myretaildata = pd.read_excel('http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx')
myretaildata = pd.read_excel('Online Retail.xlsx')

# Cleaning
myretaildata['Description'] = myretaildata['Description'].str.strip()  # removes spaces from beginning and end
myretaildata.dropna(axis=0, subset=['InvoiceNo'], inplace=True)  # removes duplicate invoice
myretaildata['InvoiceNo'] = myretaildata['InvoiceNo'].astype('str')  # converting invoice number to be string
myretaildata = myretaildata[~myretaildata['InvoiceNo'].str.contains('C')]  # remove the cancel transactions

# print(myretaildata['Country'].value_counts())

mybasket = (myretaildata[myretaildata['Country'] == "France"]
            .groupby(['InvoiceNo', 'Description'])['Quantity']
            .sum().unstack().reset_index().fillna(0)
            .set_index('InvoiceNo'))


def my_encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1


my_basket_sets = mybasket.applymap(my_encode_units)
# Remove "postage" as an item
my_basket_sets.drop('POSTAGE', inplace=True, axis=1)

my_frequent_itemsets = fpgrowth(my_basket_sets, min_support=0.07, use_colnames=True)
my_rules = association_rules(my_frequent_itemsets, metric="confidence", min_threshold=0.7)

# print(my_rules.head(100))


# csv_output(my_rules)

cust_item = "ALARM CLOCK BAKELIKE PINK"
matching_rows = my_rules[my_rules['antecedents'].apply(lambda x: cust_item in x)]
matching_ids = matching_rows.index.tolist()
recommended_items = matching_rows['consequents'].apply(lambda x: list(x)[0])
confidence_values = matching_rows['confidence']
print("Các item được recommend cho", cust_item, ":")
for item, confidence in zip(recommended_items, confidence_values):
    print("Item:", item)
    print("Confidence:", confidence)
    print()



import pandas as pd

# Load raw dataset
data = pd.read_csv('SuperStore_Sales_Dataset.csv')

# Drop duplicate rows
data.drop_duplicates(inplace=True)

data = data[['Order ID', 'Product Name', 'Category', 'Sub-Category',
             'Sales', 'Quantity', 'Profit']]

# Rename columns
data = data.rename(columns={'Order ID': 'order_id',
                            'Product Name': 'product_name',
                            'Sales': 'sales',
                            'Quantity': 'quantity',
                            'Profit': 'profit'})

print(data)
data.to_csv('Cleaned_Dataset.csv', index=False)

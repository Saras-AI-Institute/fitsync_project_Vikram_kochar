import pandas as pd

# Load the data from the CSV file
file_path = 'data/health_data.csv'
data = pd.read_csv(file_path)

# Print the first 5 rows of the dataframe
print("First 5 rows:")
print(data.head())

# Print the number of missing values in each column
print("\nMissing values in each column:")
print(data.isnull().sum())

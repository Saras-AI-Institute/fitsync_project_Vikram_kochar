from modules.processor import load_data
csv_path = 'data/health_data.csv'
cleaned_data = load_data(csv_path)
print(cleaned_data.head(20))

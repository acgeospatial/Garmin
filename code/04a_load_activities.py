import pandas as pd
from sqlalchemy import create_engine

# CSV file
csv_path = r'..\activities.csv'

# Load into DataFrame
df = pd.read_csv(csv_path)

# Connect to PostgreSQL
engine = create_engine("postgresql://postgres:mypassword@localhost:5432/mydatabase")

# Write to a table (replace 'activity_data' with your table name)
df.to_sql('activity_data', engine, if_exists='append', index=False)

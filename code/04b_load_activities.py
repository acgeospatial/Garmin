import pandas as pd
from sqlalchemy import create_engine, inspect, text

# CSV file
csv_path = r'..\activities.csv'
# Load into DataFrame
df = pd.read_csv(csv_path)
df['Activity ID'] = df['Activity ID'].astype(int)

# Connect to PostgreSQL
engine = create_engine("postgresql://postgres:mypassword@localhost:5432/mydatabase")
table_name = 'activity_data'

# Check if table exists
inspector = inspect(engine)
table_exists = inspector.has_table(table_name)

if table_exists:
    # Fetch existing IDs
    with engine.begin() as conn:
        existing_ids = {
            row[0] for row in conn.execute(text(f'SELECT "Activity ID" FROM {table_name}'))
        }
    
    # Filter new records
    new_df = df[~df['Activity ID'].isin(existing_ids)]
else:
    # Table doesn't exist yet — insert all data
    new_df = df.copy()

# Insert new records
if not new_df.empty:
    new_df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"Inserted {len(new_df)} new activities.")
else:
    print("No new activities to insert.")

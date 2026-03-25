import pandas as pd
import numpy as np
from datetime import datetime, timedelta


np.random.seed(42)

# Constants
NUM_DAYS = 365
START_DATE = datetime(2025, 1, 1)

# Generate date range

dates = [START_DATE + timedelta(days=i) for i in range(NUM_DAYS)]



# Generate realistic data
steps = np.random.normal(loc=8500, scale=1000, size=NUM_DAYS).clip(3000, 18000)
sleep_hours = np.random.normal(loc=7.2, scale=1, size=NUM_DAYS).clip(4.2, 9.5)
heart_rate_bpm = np.random.normal(loc=68, scale=10, size=NUM_DAYS).clip(48, 110)
calories_burnt = np.random.uniform(1800, 4200, NUM_DAYS)
active_minutes = np.random.uniform(20, 180, NUM_DAYS)

# Introduce 5% missing values
for data in [steps, sleep_hours, heart_rate_bpm, calories_burnt, active_minutes]:
    mask = np.random.rand(NUM_DAYS) < 0.05
    data[mask] = np.nan

# Create DataFrame
data = pd.DataFrame({
    'date': dates,
    'steps': steps,
    'sleep_hours': sleep_hours,
    'heart_rate_bpm': heart_rate_bpm,
    'calories_burnt': calories_burnt,
    'active_minutes': active_minutes
})

# Save to CSV
data.to_csv('data/health_data.csv', index=False)

print("Data generated and saved to health_data.csv")
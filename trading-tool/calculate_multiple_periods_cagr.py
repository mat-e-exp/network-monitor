import csv
from datetime import datetime

# Read the CSV data
data = []
with open('ftse100.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if len(row) >= 5:
            try:
                data.append({
                    'date': row[0],
                    'open': float(row[1]),
                    'high': float(row[2]),
                    'low': float(row[3]),
                    'close': float(row[4])
                })
            except ValueError:
                continue

print(f"Loaded {len(data)} trading days")

# Group data by year
yearly_data = {}

for record in data:
    try:
        date_part = record['date'].split()[0]
        month, day, year = date_part.split('/')
        year = int(year)
        
        if year not in yearly_data:
            yearly_data[year] = []
        yearly_data[year].append(record)
    except (ValueError, IndexError):
        continue

# Get sorted years and their end prices
years_sorted = sorted(yearly_data.keys())
year_end_prices = {}

for year in years_sorted:
    year_records = yearly_data[year]
    if year_records:
        year_end_prices[year] = year_records[-1]['close']

# Current year (latest year in data)
current_year = max(years_sorted)
current_price = year_end_prices[current_year]

print(f"Current year: {current_year}")
print(f"Current price: {current_price:.1f}")

# Calculate CAGR for different periods
periods = [5, 10, 15, 20, 25]
cagr_results = []

print(f"\n=== CAGR FOR DIFFERENT PERIODS ===")
print("Period\tStart Year\tStart Price\tEnd Price\tCAGR%")
print("-" * 60)

for period in periods:
    start_year = current_year - period
    
    if start_year in year_end_prices:
        start_price = year_end_prices[start_year]
        end_price = current_price
        
        # CAGR = (End Value / Start Value)^(1/years) - 1
        cagr = (pow(end_price / start_price, 1/period) - 1) * 100
        cagr_results.append(cagr)
        
        print(f"{period} years\t{start_year}\t\t{start_price:.1f}\t\t{end_price:.1f}\t\t{cagr:.2f}%")
    else:
        print(f"{period} years\t{start_year}\t\tNo data available")

# Calculate average CAGR across all periods
if cagr_results:
    average_cagr = sum(cagr_results) / len(cagr_results)
    
    print(f"\n=== SUMMARY ===")
    print(f"CAGR Results: {[f'{x:.2f}%' for x in cagr_results]}")
    print(f"Average CAGR across all periods: {average_cagr:.2f}%")
    
    # Show individual results clearly
    print(f"\nIndividual Period Results:")
    for i, period in enumerate(periods):
        if i < len(cagr_results):
            print(f"Last {period} years: {cagr_results[i]:.2f}%")
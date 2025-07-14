import csv
import math

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

# Current year and price
current_year = max(years_sorted)
current_price = year_end_prices[current_year]

print(f"Current year: {current_year}")
print(f"Current FTSE level: {current_price:.1f}")

# Calculate CAGR for different periods
periods = [5, 10, 15, 20, 25]
cagr_data = []

print(f"\n=== DETAILED CAGR ANALYSIS ===")
print("Period\tStart Year\tStart Price\tEnd Price\tCAGR%\tTotal Return%")
print("-" * 75)

for period in periods:
    start_year = current_year - period
    
    if start_year in year_end_prices:
        start_price = year_end_prices[start_year]
        end_price = current_price
        
        # CAGR = (End Value / Start Value)^(1/years) - 1
        cagr = (pow(end_price / start_price, 1/period) - 1) * 100
        
        # Total return
        total_return = ((end_price - start_price) / start_price) * 100
        
        cagr_data.append({
            'period': period,
            'start_year': start_year,
            'start_price': start_price,
            'end_price': end_price,
            'cagr': cagr,
            'total_return': total_return
        })
        
        print(f"{period} years\t{start_year}\t\t{start_price:.1f}\t\t{end_price:.1f}\t\t{cagr:.2f}%\t\t{total_return:.1f}%")

# Calculate statistics
cagr_values = [item['cagr'] for item in cagr_data]

if cagr_values:
    # Mean
    mean_cagr = sum(cagr_values) / len(cagr_values)
    
    # Standard deviation
    variance = sum((x - mean_cagr) ** 2 for x in cagr_values) / len(cagr_values)
    std_dev = math.sqrt(variance)
    
    # Min and Max
    min_cagr = min(cagr_values)
    max_cagr = max(cagr_values)
    
    print(f"\n=== STATISTICAL ANALYSIS ===")
    print(f"CAGR Values: {[f'{x:.2f}%' for x in cagr_values]}")
    print(f"Mean CAGR: {mean_cagr:.2f}%")
    print(f"Standard Deviation: {std_dev:.2f}%")
    print(f"Minimum CAGR: {min_cagr:.2f}%")
    print(f"Maximum CAGR: {max_cagr:.2f}%")
    print(f"Range: {max_cagr - min_cagr:.2f}%")
    
    # Show how far each value is from mean in terms of standard deviations
    print(f"\n=== DEVIATION FROM MEAN ===")
    print("Period\tCAGR%\tDeviation from Mean\tZ-Score")
    print("-" * 50)
    
    for item in cagr_data:
        deviation = item['cagr'] - mean_cagr
        z_score = deviation / std_dev if std_dev > 0 else 0
        print(f"{item['period']} years\t{item['cagr']:.2f}%\t{deviation:+.2f}%\t\t{z_score:+.2f}")
    
    # Confidence intervals (assuming normal distribution)
    print(f"\n=== CONFIDENCE INTERVALS ===")
    print(f"68% of values within: {mean_cagr - std_dev:.2f}% to {mean_cagr + std_dev:.2f}%")
    print(f"95% of values within: {mean_cagr - 2*std_dev:.2f}% to {mean_cagr + 2*std_dev:.2f}%")
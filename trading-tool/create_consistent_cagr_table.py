import csv

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

# Current settings
current_year = 2025
current_ftse = 8925.0  # As specified by user
consistent_cagr = 3.6  # Use 3.6% for all calculations

# Timeframes to analyze
timeframes = [5, 10, 15, 20, 25, 30, 35, 40]

print("Start\tYears\tCAGR\tEnd\tActual\tDifference")
print("-" * 60)

for years in timeframes:
    start_year = current_year - years
    
    if start_year in year_end_prices:
        start_price = year_end_prices[start_year]
        
        # Use consistent CAGR of 3.6%
        cagr = consistent_cagr
        
        # End is always current FTSE
        end_price = current_ftse
        
        # Actual = start price grown at consistent 3.6% CAGR for the number of years
        actual_price = start_price * pow(1 + (cagr/100), years)
        
        # Difference between actual theoretical value and current end value
        difference = actual_price - end_price
        
        print(f"{start_price:.1f}\t{years}\t{cagr:.1f}%\t{end_price:.0f}\t{actual_price:.0f}\t{difference:+.0f}")
    else:
        print(f"N/A\t{years}\t{consistent_cagr:.1f}%\t{current_ftse:.0f}\tN/A\tN/A")

print(f"\nExplanation:")
print(f"- All periods use consistent {consistent_cagr}% CAGR")
print(f"- Start: Historical FTSE price from each timeframe")
print(f"- Actual: What start price would be worth today at {consistent_cagr}% CAGR")
print(f"- Difference: Shows over/under performance vs {consistent_cagr}% growth")
print(f"- Positive difference = actual growth exceeded {consistent_cagr}%")
print(f"- Negative difference = actual growth was below {consistent_cagr}%")
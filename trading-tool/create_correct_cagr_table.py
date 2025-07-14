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

# Timeframes to analyze
timeframes = [5, 10, 15, 20, 25, 30, 35, 40]

print("Start\tCAGR\tEnd\tActual\tDifference")
print("-" * 50)

for years in timeframes:
    start_year = current_year - years
    
    if start_year in year_end_prices:
        start_price = year_end_prices[start_year]
        
        # Calculate CAGR from start to current
        cagr = (pow(current_ftse / start_price, 1/years) - 1) * 100
        
        # End is always current FTSE
        end_price = current_ftse
        
        # Actual = what the start price would be worth today if it grew at this CAGR
        # This should equal end_price, but let's calculate it explicitly
        actual_price = start_price * pow(1 + (cagr/100), years)
        
        # Difference between actual and end (should be ~0)
        difference = actual_price - end_price
        
        print(f"{years}\t{cagr:.2f}%\t{end_price:.0f}\t{actual_price:.0f}\t{difference:+.0f}")
    else:
        print(f"{years}\tNo data\t{current_ftse:.0f}\tN/A\tN/A")

print(f"\nDetailed breakdown:")
print("Years\tStart Year\tStart Price\tCAGR\tEnd\tActual\tDifference")
print("-" * 70)

for years in timeframes:
    start_year = current_year - years
    
    if start_year in year_end_prices:
        start_price = year_end_prices[start_year]
        cagr = (pow(current_ftse / start_price, 1/years) - 1) * 100
        end_price = current_ftse
        actual_price = start_price * pow(1 + (cagr/100), years)
        difference = actual_price - end_price
        
        print(f"{years}\t{start_year}\t\t{start_price:.1f}\t\t{cagr:.2f}%\t{end_price:.0f}\t{actual_price:.0f}\t{difference:+.0f}")
    else:
        print(f"{years}\t{start_year}\t\tNo data\t\tN/A\t{current_ftse:.0f}\tN/A\tN/A")
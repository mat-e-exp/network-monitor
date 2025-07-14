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

print(f"Actual FTSE level now: {current_price:.1f}")

# Calculate theoretical FTSE levels
periods = [5, 10, 15, 20, 25]

print(f"\n=== THEORETICAL FTSE LEVELS WITH CONSISTENT CAGR ===")
print("Period\tStart Year\tStart Price\tActual CAGR\tTheoretical FTSE\tActual FTSE\tDifference")
print("-" * 90)

for period in periods:
    start_year = current_year - period
    
    if start_year in year_end_prices:
        start_price = year_end_prices[start_year]
        
        # Calculate actual CAGR
        actual_cagr = (pow(current_price / start_price, 1/period) - 1) * 100
        
        # Calculate what FTSE would be with consistent CAGR growth
        # Formula: Future Value = Present Value * (1 + r)^n
        theoretical_price = start_price * pow(1 + (actual_cagr/100), period)
        
        # Difference
        difference = theoretical_price - current_price
        difference_pct = (difference / current_price) * 100
        
        print(f"{period} years\t{start_year}\t\t{start_price:.1f}\t\t{actual_cagr:.2f}%\t\t{theoretical_price:.1f}\t\t{current_price:.1f}\t\t{difference:+.1f} ({difference_pct:+.1f}%)")

print(f"\n=== ANALYSIS ===")
print("Note: The 'Theoretical FTSE' shows where the index would be if it had grown")
print("at a perfectly consistent compound rate equal to the actual CAGR for that period.")
print("Since markets are volatile, the theoretical and actual values should be identical")
print("(or very close due to rounding).")

# Let's also show what would happen with different consistent growth rates
print(f"\n=== COMPARISON WITH DIFFERENT CONSISTENT GROWTH RATES ===")
test_rates = [2.0, 3.0, 4.0, 5.0, 6.0]  # Different CAGR rates to test

print("If FTSE had grown at consistent rates from different starting points:")
print("Start Year\tStart Price\t2% CAGR\t3% CAGR\t4% CAGR\t5% CAGR\t6% CAGR")
print("-" * 80)

for period in periods:
    start_year = current_year - period
    if start_year in year_end_prices:
        start_price = year_end_prices[start_year]
        
        results = []
        for rate in test_rates:
            theoretical = start_price * pow(1 + (rate/100), period)
            results.append(f"{theoretical:.0f}")
        
        print(f"{start_year}\t\t{start_price:.1f}\t\t{results[0]}\t{results[1]}\t{results[2]}\t{results[3]}\t{results[4]}")

print(f"\nActual current FTSE: {current_price:.1f}")

# Show which consistent rate would have gotten us to current level
print(f"\n=== REQUIRED CONSISTENT CAGR TO REACH CURRENT LEVEL ===")
print("Start Year\tStart Price\tRequired CAGR\tActual CAGR\tDifference")
print("-" * 65)

for period in periods:
    start_year = current_year - period
    if start_year in year_end_prices:
        start_price = year_end_prices[start_year]
        
        # This is just the actual CAGR (since we end up at current price)
        required_cagr = (pow(current_price / start_price, 1/period) - 1) * 100
        actual_cagr = required_cagr  # Same thing
        
        print(f"{start_year}\t\t{start_price:.1f}\t\t{required_cagr:.2f}%\t\t{actual_cagr:.2f}%\t\t0.00%")
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
                    'close': float(row[4])
                })
            except ValueError:
                continue

# Use actual current FTSE 100 price
actual_current_value = 8900

print("=== UPDATED ANALYSIS WITH ACTUAL FTSE 100 PRICE ===")
print(f"Actual current FTSE 100: 8,900")
print(f"Data file shows: {data[-1]['close']:.1f} (outdated)")
print()

# Find starting values for different periods
periods = [
    {"start_year": 2020, "description": "5-year period"},
    {"start_year": 2015, "description": "10-year period"},
    {"start_year": 2010, "description": "15-year period"},
    {"start_year": 2005, "description": "20-year period"},
    {"start_year": 1985, "description": "40-year period"}
]

# Get starting values
start_values = {}
for period in periods:
    start_year = period["start_year"]
    for record in data:
        date_part = record['date'].split()[0]
        try:
            month, day, year = date_part.split('/')
            year = int(year)
            if year == start_year:
                start_values[start_year] = record['close']
                break
        except (ValueError, IndexError):
            continue

print("=== ACTUAL PERFORMANCE WITH CURRENT PRICE ===")
print("Period\t\tStart Value\tCurrent Value\tActual CAGR\tTotal Return")
print("-" * 80)

updated_cagrs = {}
for period in periods:
    start_year = period["start_year"]
    if start_year in start_values:
        start_value = start_values[start_year]
        years = 2025 - start_year
        
        # Calculate actual CAGR with current price
        actual_cagr = (pow(actual_current_value / start_value, 1/years) - 1) * 100
        total_return = ((actual_current_value - start_value) / start_value) * 100
        
        updated_cagrs[start_year] = actual_cagr
        
        print(f"{period['description']:<15}\t{start_value:.1f}\t\t{actual_current_value}\t\t{actual_cagr:.2f}%\t\t{total_return:.1f}%")

print()
print("=== THEORETICAL VALUES USING ORIGINAL DATA CAGRs ===")

# Original CAGRs from the data analysis
original_cagrs = {
    2020: 1.67,
    2015: 2.35,
    2010: 2.75,
    2005: 2.70,
    1985: 5.07
}

print("Period\t\tOriginal CAGR\tTheoretical Value\tActual Value\tDifference")
print("-" * 85)

for period in periods:
    start_year = period["start_year"]
    if start_year in start_values and start_year in original_cagrs:
        start_value = start_values[start_year]
        years = 2025 - start_year
        original_cagr = original_cagrs[start_year]
        
        # Calculate theoretical value using original CAGR
        theoretical_value = start_value * (1 + original_cagr/100) ** years
        difference = actual_current_value - theoretical_value
        difference_percent = (difference / theoretical_value) * 100
        
        print(f"{period['description']:<15}\t{original_cagr:.2f}%\t\t{theoretical_value:.0f}\t\t{actual_current_value}\t\t{difference:+.0f} ({difference_percent:+.1f}%)")

print()
print("=== INVESTMENT IMPLICATIONS ===")
print("£1,000 invested at different periods:")
print()

for period in periods:
    start_year = period["start_year"]
    if start_year in start_values:
        start_value = start_values[start_year]
        years = 2025 - start_year
        
        # Actual investment value
        actual_investment = 1000 * (actual_current_value / start_value)
        
        # Theoretical investment using original CAGR
        if start_year in original_cagrs:
            original_cagr = original_cagrs[start_year]
            theoretical_investment = 1000 * (1 + original_cagr/100) ** years
            difference = actual_investment - theoretical_investment
            
            print(f"{period['description']} ({start_year}):")
            print(f"  Actual return: £{actual_investment:,.0f}")
            print(f"  Expected (old CAGR): £{theoretical_investment:,.0f}")
            print(f"  Difference: £{difference:+,.0f}")
            print(f"  Actual CAGR: {updated_cagrs[start_year]:.2f}% vs Expected {original_cagr:.2f}%")
            print()

print("=== KEY INSIGHTS ===")
print()

# Compare updated vs original CAGRs
print("Updated CAGRs with actual current price:")
for start_year in sorted(updated_cagrs.keys()):
    original = original_cagrs[start_year]
    updated = updated_cagrs[start_year]
    improvement = updated - original
    years = 2025 - start_year
    
    print(f"• {years}-year period: {updated:.2f}% (vs {original:.2f}% in data) - improvement: {improvement:+.2f}%")

print()
print("The FTSE 100 at 8,900 represents BETTER performance than the historical data suggested\!")


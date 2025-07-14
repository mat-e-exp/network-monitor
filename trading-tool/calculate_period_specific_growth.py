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

# Find starting values for each period
periods = [
    {"start_year": 2020, "cagr": 1.67, "years": 5, "description": "5-year CAGR from 2020"},
    {"start_year": 2015, "cagr": 2.35, "years": 10, "description": "10-year CAGR from 2015"},
    {"start_year": 2010, "cagr": 2.75, "years": 15, "description": "15-year CAGR from 2010"},
    {"start_year": 2005, "cagr": 2.70, "years": 20, "description": "20-year CAGR from 2005"}
]

# Get current value (2025)
current_value = None
for record in data:
    date_part = record['date'].split()[0]
    try:
        month, day, year = date_part.split('/')
        year = int(year)
        if year == 2025:
            current_value = record['close']
            break
    except (ValueError, IndexError):
        continue

print("=== FTSE 100 GROWTH SCENARIOS FROM SPECIFIC START POINTS ===")
print(f"Current FTSE 100 value (2025): {current_value:.1f}")
print()

for period in periods:
    start_year = period["start_year"]
    cagr = period["cagr"]
    years = period["years"]
    description = period["description"]
    
    # Find starting value for this year
    start_value = None
    for record in data:
        date_part = record['date'].split()[0]
        try:
            month, day, year = date_part.split('/')
            year = int(year)
            if year == start_year:
                start_value = record['close']
                break
        except (ValueError, IndexError):
            continue
    
    if start_value is None:
        print(f"No data found for {start_year}")
        continue
    
    # Calculate theoretical value from start year to 2025
    years_to_2025 = 2025 - start_year
    theoretical_value = start_value * (1 + cagr/100) ** years_to_2025
    
    # Calculate actual performance from start year to 2025
    actual_cagr = (pow(current_value / start_value, 1/years_to_2025) - 1) * 100
    
    # Calculate differences
    difference = theoretical_value - current_value
    difference_percent = (difference / current_value) * 100
    
    # Investment implications
    investment_theoretical = 1000 * (theoretical_value / start_value)
    investment_actual = 1000 * (current_value / start_value)
    investment_difference = investment_theoretical - investment_actual
    
    print(f"=== {description.upper()} ===")
    print(f"Starting value ({start_year}): {start_value:.1f}")
    print(f"Period analyzed: {start_year}-{start_year + years}")
    print(f"CAGR from that period: {cagr:.2f}%")
    print(f"Years to project forward: {years_to_2025}")
    print()
    print(f"Theoretical FTSE 100 today: {theoretical_value:.1f}")
    print(f"Actual FTSE 100 today: {current_value:.1f}")
    print(f"Difference: {difference:+.1f} points ({difference_percent:+.1f}%)")
    print()
    print(f"Actual CAGR achieved ({start_year}-2025): {actual_cagr:.2f}%")
    print(f"vs Period CAGR: {cagr:.2f}%")
    print(f"Performance gap: {actual_cagr - cagr:+.2f}%")
    print()
    print(f"£1,000 investment from {start_year}:")
    print(f"Theoretical ({cagr:.2f}%): £{investment_theoretical:,.0f}")
    print(f"Actual performance: £{investment_actual:,.0f}")
    print(f"Difference: £{investment_difference:+,.0f}")
    print()
    
    if theoretical_value > current_value:
        print(f"📈 FTSE would be {difference:.1f} points HIGHER")
    else:
        print(f"📉 FTSE would be {abs(difference):.1f} points LOWER")
    
    print("-" * 70)
    print()

# Summary comparison
print("=== SUMMARY COMPARISON ===")
print("Start Year\tPeriod CAGR\tTheoretical Value\tActual Value\tDifference")
print("-" * 80)

results = []
for period in periods:
    start_year = period["start_year"]
    cagr = period["cagr"]
    
    # Find starting value
    start_value = None
    for record in data:
        date_part = record['date'].split()[0]
        try:
            month, day, year = date_part.split('/')
            year = int(year)
            if year == start_year:
                start_value = record['close']
                break
        except (ValueError, IndexError):
            continue
    
    if start_value is None:
        continue
    
    years_to_2025 = 2025 - start_year
    theoretical_value = start_value * (1 + cagr/100) ** years_to_2025
    difference = theoretical_value - current_value
    
    results.append({
        'start_year': start_year,
        'cagr': cagr,
        'theoretical_value': theoretical_value,
        'difference': difference
    })
    
    print(f"{start_year}\t\t{cagr:.2f}%\t\t{theoretical_value:.1f}\t\t{current_value:.1f}\t\t{difference:+.1f}")

print()
print("=== KEY INSIGHTS ===")
print()

best_scenario = max(results, key=lambda x: x['theoretical_value'])
worst_scenario = min(results, key=lambda x: x['theoretical_value'])

print(f"• HIGHEST theoretical value: {best_scenario['theoretical_value']:.1f} (using {best_scenario['cagr']:.2f}% from {best_scenario['start_year']})")
print(f"• LOWEST theoretical value: {worst_scenario['theoretical_value']:.1f} (using {worst_scenario['cagr']:.2f}% from {worst_scenario['start_year']})")
print(f"• Range between scenarios: {best_scenario['theoretical_value'] - worst_scenario['theoretical_value']:.1f} points")
print()

# Check which is closest to actual
closest = min(results, key=lambda x: abs(x['difference']))
print(f"• Closest to actual value: {closest['cagr']:.2f}% CAGR from {closest['start_year']} (difference: {closest['difference']:+.1f} points)")


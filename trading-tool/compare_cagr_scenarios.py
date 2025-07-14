import csv

# Read the CSV data to get 1985 starting value and current value
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

# Find 1985 starting value and current value
start_1985 = None
current_2025 = None

for record in data:
    date_part = record['date'].split()[0]
    try:
        month, day, year = date_part.split('/')
        year = int(year)
        
        if year == 1985 and start_1985 is None:
            start_1985 = record['close']
        
        if year == 2025:
            current_2025 = record['close']
    except (ValueError, IndexError):
        continue

# Define the different CAGR scenarios
scenarios = [
    {"name": "Historical Long-term", "cagr": 5.07, "description": "Actual 40-year average"},
    {"name": "20-year Performance", "cagr": 2.70, "description": "2005-2025 average"},
    {"name": "15-year Performance", "cagr": 2.75, "description": "2010-2025 average"},
    {"name": "10-year Performance", "cagr": 2.35, "description": "2015-2025 average"},
    {"name": "5-year Performance", "cagr": 1.67, "description": "2020-2025 average"},
]

years = 2025 - 1985  # 40 years from 1985 to 2025

print("=== FTSE 100 SCENARIOS: WHERE WOULD WE BE TODAY? ===")
print(f"Starting from 1985 value: {start_1985:.1f}")
print(f"Actual current value: {current_2025:.1f}")
print(f"Time period: {years} years (1985-2025)")
print()

print("Scenario\t\t\tCAGR\t\tTheoretical Value\tDifference vs Actual")
print("-" * 95)

results = []

for scenario in scenarios:
    cagr = scenario["cagr"]
    theoretical_value = start_1985 * (1 + cagr/100) ** years
    difference = theoretical_value - current_2025
    difference_percent = (difference / current_2025) * 100
    
    results.append({
        "name": scenario["name"],
        "cagr": cagr,
        "theoretical_value": theoretical_value,
        "difference": difference,
        "difference_percent": difference_percent,
        "description": scenario["description"]
    })
    
    print(f"{scenario['name']:<25}\t{cagr:.2f}%\t\t{theoretical_value:,.0f}\t\t{difference:+,.0f} ({difference_percent:+.1f}%)")

print()
print("=== DETAILED ANALYSIS ===")
print()

for result in results:
    print(f"{result['name']} ({result['description']}):")
    print(f"  CAGR: {result['cagr']:.2f}%")
    print(f"  Theoretical FTSE 100 today: {result['theoretical_value']:,.0f}")
    print(f"  vs Actual: {result['difference']:+,.0f} points ({result['difference_percent']:+.1f}%)")
    
    # Calculate investment implications
    investment_value = 1000 * (result['theoretical_value'] / start_1985)
    actual_investment = 1000 * (current_2025 / start_1985)
    investment_diff = investment_value - actual_investment
    
    print(f"  £1,000 investment: £{investment_value:,.0f} vs £{actual_investment:,.0f} (difference: £{investment_diff:+,.0f})")
    print()

# Show ranking
print("=== RANKING BY PERFORMANCE ===")
sorted_results = sorted(results, key=lambda x: x['theoretical_value'], reverse=True)

for i, result in enumerate(sorted_results, 1):
    status = "HIGHER" if result['difference'] > 0 else "LOWER"
    print(f"{i}. {result['name']}: {result['theoretical_value']:,.0f} ({status} than actual)")

print()
print("=== KEY INSIGHTS ===")
print()

best_scenario = max(results, key=lambda x: x['theoretical_value'])
worst_scenario = min(results, key=lambda x: x['theoretical_value'])

print(f"• If the FTSE had maintained its BEST recent performance ({best_scenario['cagr']:.2f}% CAGR),")
print(f"  it would be at {best_scenario['theoretical_value']:,.0f} today")
print()
print(f"• If the FTSE had maintained its WORST recent performance ({worst_scenario['cagr']:.2f}% CAGR),")
print(f"  it would be at {worst_scenario['theoretical_value']:,.0f} today")
print()
print(f"• The difference between best and worst scenarios: {best_scenario['theoretical_value'] - worst_scenario['theoretical_value']:,.0f} points")
print()
print(f"• Actual FTSE 100 is closest to the {min(results, key=lambda x: abs(x['difference']))['name']} scenario")


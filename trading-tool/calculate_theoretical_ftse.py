import csv
from datetime import datetime

# Read the CSV data to get actual values
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

print("=== THEORETICAL FTSE 100 CALCULATION ===")
print()

# Calculate years from 1985 to 2025
years = 2025 - 1985
cagr = 5.07  # The calculated CAGR

print(f"Starting value (1985): {start_1985:.1f}")
print(f"Current value (2025): {current_2025:.1f}")
print(f"Years elapsed: {years}")
print(f"CAGR to apply: {cagr:.2f}%")
print()

# Calculate theoretical value
# Formula: Future Value = Present Value × (1 + growth_rate)^years
theoretical_value = start_1985 * (1 + cagr/100) ** years

print(f"=== CALCULATION ===")
print(f"Theoretical FTSE 100 = {start_1985:.1f} × (1 + {cagr:.2f}/100)^{years}")
print(f"Theoretical FTSE 100 = {start_1985:.1f} × (1.{cagr:.0f})^{years}")
print(f"Theoretical FTSE 100 = {start_1985:.1f} × {(1 + cagr/100) ** years:.4f}")
print(f"Theoretical FTSE 100 = {theoretical_value:.1f}")
print()

# Compare with actual
actual_growth = ((current_2025 - start_1985) / start_1985) * 100
actual_cagr = (pow(current_2025 / start_1985, 1/years) - 1) * 100
difference = current_2025 - theoretical_value
difference_percent = (difference / theoretical_value) * 100

print(f"=== COMPARISON ===")
print(f"Theoretical value (5.07% CAGR): {theoretical_value:.1f}")
print(f"Actual current value: {current_2025:.1f}")
print(f"Difference: {difference:+.1f} points ({difference_percent:+.1f}%)")
print()

print(f"=== ANALYSIS ===")
print(f"Actual total growth (1985-2025): {actual_growth:.1f}%")
print(f"Actual CAGR achieved: {actual_cagr:.2f}%")
print()

if current_2025 > theoretical_value:
    print(f"✅ FTSE 100 has OUTPERFORMED the steady {cagr:.2f}% CAGR by {difference:.1f} points")
else:
    print(f"❌ FTSE 100 has UNDERPERFORMED the steady {cagr:.2f}% CAGR by {abs(difference):.1f} points")

# Show what this means in investment terms
print()
print(f"=== INVESTMENT IMPLICATION ===")
print(f"£1,000 invested in 1985 at steady {cagr:.2f}% CAGR would be worth:")
investment_value = 1000 * (1 + cagr/100) ** years
print(f"£{investment_value:,.0f}")

actual_investment = 1000 * (current_2025 / start_1985)
print(f"£1,000 invested in actual FTSE 100 in 1985 would be worth:")
print(f"£{actual_investment:,.0f}")

print(f"Difference: £{actual_investment - investment_value:+,.0f}")


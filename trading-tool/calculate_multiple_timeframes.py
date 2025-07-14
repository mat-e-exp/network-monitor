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
                    'close': float(row[4])
                })
            except ValueError:
                continue

# Find values for different timeframes
timeframes = [5, 10, 15, 20]
current_year = 2025
cagr = 5.07

print("=== FTSE 100 PERFORMANCE vs 5.07% CAGR ACROSS TIMEFRAMES ===")
print()

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

print(f"Current FTSE 100 value (2025): {current_value:.1f}")
print()

for timeframe in timeframes:
    start_year = current_year - timeframe
    
    # Find starting value for this timeframe
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
    
    # Calculate theoretical value
    theoretical_value = start_value * (1 + cagr/100) ** timeframe
    
    # Calculate actual performance
    actual_cagr = (pow(current_value / start_value, 1/timeframe) - 1) * 100
    difference = current_value - theoretical_value
    difference_percent = (difference / theoretical_value) * 100
    
    # Calculate investment returns
    investment_theoretical = 1000 * (1 + cagr/100) ** timeframe
    investment_actual = 1000 * (current_value / start_value)
    investment_difference = investment_actual - investment_theoretical
    
    print(f"=== {timeframe} YEAR PERFORMANCE ({start_year}-{current_year}) ===")
    print(f"Starting value ({start_year}): {start_value:.1f}")
    print(f"Current value ({current_year}): {current_value:.1f}")
    print()
    print(f"Theoretical value (5.07% CAGR): {theoretical_value:.1f}")
    print(f"Actual value: {current_value:.1f}")
    print(f"Difference: {difference:+.1f} points ({difference_percent:+.1f}%)")
    print()
    print(f"Actual CAGR achieved: {actual_cagr:.2f}%")
    print(f"vs Target CAGR: 5.07%")
    print(f"Performance gap: {actual_cagr - cagr:+.2f}%")
    print()
    print(f"£1,000 investment results:")
    print(f"Theoretical (5.07%): £{investment_theoretical:,.0f}")
    print(f"Actual FTSE 100: £{investment_actual:,.0f}")
    print(f"Difference: £{investment_difference:+,.0f}")
    print()
    
    if current_value > theoretical_value:
        print(f"✅ OUTPERFORMED by {difference:.1f} points")
    else:
        print(f"❌ UNDERPERFORMED by {abs(difference):.1f} points")
    
    print("-" * 60)
    print()

# Summary table
print("=== SUMMARY TABLE ===")
print("Timeframe\tActual CAGR\tTarget CAGR\tPerformance Gap\tOutperform/Under")
print("-" * 80)

for timeframe in timeframes:
    start_year = current_year - timeframe
    
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
    
    # Calculate performance
    actual_cagr = (pow(current_value / start_value, 1/timeframe) - 1) * 100
    theoretical_value = start_value * (1 + cagr/100) ** timeframe
    difference = current_value - theoretical_value
    
    performance_gap = actual_cagr - cagr
    status = "OUTPERFORM" if current_value > theoretical_value else "UNDERPERFORM"
    
    print(f"{timeframe} years\t\t{actual_cagr:.2f}%\t\t5.07%\t\t{performance_gap:+.2f}%\t\t{status}")


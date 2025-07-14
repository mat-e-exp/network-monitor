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

print("=== REAL EXAMPLE: March 2025 NEW HIGH CYCLE ===")
print()

# Find the March 3, 2025 new high and show the cycle
target_date = "3/3/2025"
start_idx = None

for i, day in enumerate(data):
    if target_date in day['date']:
        start_idx = i
        break

if start_idx:
    print("Step-by-step breakdown of March 3, 2025 new high cycle:")
    print()
    print("Date\t\t\tOpen\tHigh\tLow\tClose\tNotes")
    print("-" * 85)
    
    # Show the new high day
    day = data[start_idx]
    print(f"{day['date']:<20}\t{day['open']:.1f}\t{day['high']:.1f}\t{day['low']:.1f}\t{day['close']:.1f}\t← NEW HIGH: {day['high']:.1f}")
    
    # Track forward to find the complete cycle
    new_high_value = day['high']
    peak_value = new_high_value
    peak_date = day['date']
    trough_value = new_high_value
    trough_date = day['date']
    
    # Show next 20 days or until cycle ends
    for i in range(start_idx + 1, min(start_idx + 21, len(data))):
        day = data[i]
        
        notes = ""
        
        # Update peak
        if day['high'] > peak_value:
            peak_value = day['high']
            peak_date = day['date']
            notes += f"NEW PEAK: {day['high']:.1f}"
        
        # Update trough
        if day['low'] < trough_value:
            trough_value = day['low']
            trough_date = day['date']
            if notes:
                notes += ", "
            notes += f"NEW TROUGH: {day['low']:.1f}"
        
        # Check if cycle ends
        if day['low'] < new_high_value:
            notes += " → CYCLE ENDS (below new high)"
            print(f"{day['date']:<20}\t{day['open']:.1f}\t{day['high']:.1f}\t{day['low']:.1f}\t{day['close']:.1f}\t{notes}")
            break
        
        print(f"{day['date']:<20}\t{day['open']:.1f}\t{day['high']:.1f}\t{day['low']:.1f}\t{day['close']:.1f}\t{notes}")
    
    print()
    print("=== FINAL CALCULATION ===")
    print(f"New High Date: {data[start_idx]['date']}")
    print(f"New High Value: {new_high_value:.1f} (HIGH of new high day)")
    print(f"Peak Date: {peak_date}")
    print(f"Peak Value: {peak_value:.1f} (highest HIGH after new high)")
    print(f"Trough Date: {trough_date}")
    print(f"Trough Value: {trough_value:.1f} (lowest LOW in the cycle)")
    print()
    print(f"Pullback Calculation:")
    print(f"Points: {peak_value:.1f} - {trough_value:.1f} = {peak_value - trough_value:.1f} points")
    print(f"Percentage: ({peak_value:.1f} - {trough_value:.1f}) / {peak_value:.1f} * 100 = {((peak_value - trough_value) / peak_value) * 100:.2f}%")


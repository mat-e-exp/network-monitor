import csv

# Read first 20 rows to show the data structure
data = []
with open('ftse100.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for i, row in enumerate(reader):
        if i < 20 and len(row) >= 5:
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

print("=== DATA STRUCTURE ===")
print("Columns: Date, Open, High, Low, Close, Volume")
print("\nFirst 10 rows of data:")
print("Date\t\t\tOpen\tHigh\tLow\tClose")
print("-" * 60)
for row in data[:10]:
    print(f"{row['date']:<20}\t{row['open']:.1f}\t{row['high']:.1f}\t{row['low']:.1f}\t{row['close']:.1f}")

print("\n=== METHODOLOGY FOR PULLBACK CALCULATION ===")
print("""
1. NEW HIGH IDENTIFICATION:
   - Compare each day's HIGH to the running all-time high
   - If today's HIGH > previous all-time high → New High Event
   - Use the HIGH price as the new high level

2. PEAK TRACKING:
   - Starting from new high date, track forward through subsequent days
   - Record the highest HIGH value reached after the new high
   - This becomes the "peak" for pullback calculation

3. TROUGH TRACKING:
   - From the peak date forward, track the lowest LOW value
   - Continue until price drops below the original new high level
   - This lowest LOW becomes the "trough"

4. PULLBACK CALCULATION:
   - Pullback Points = Peak HIGH - Trough LOW
   - Pullback % = (Peak HIGH - Trough LOW) / Peak HIGH * 100

5. CYCLE END:
   - Cycle ends when any day's LOW drops below the original new high
   - This marks a complete "new high cycle"
""")

print("=== EXAMPLE CALCULATION ===")
print("""
Example scenario:
Day 1: New high at 8000 (using HIGH of that day)
Day 2: HIGH reaches 8050 (this becomes the peak)
Day 3: LOW drops to 7950
Day 4: LOW drops to 7980 (still above original 8000)
Day 5: LOW drops to 7990 (still above original 8000)  
Day 6: LOW drops to 7950 (this is the trough - lowest point)
Day 7: LOW drops to 7980 (still in cycle)
Day 8: LOW drops to 7990 (still in cycle)
Day 9: LOW drops to 7995 (still above 8000)
Day 10: LOW drops to 7990 (still above 8000)
Day 11: LOW drops to 7995 (cycle continues...)
...
Day N: LOW drops to 7850 (below 8000) → CYCLE ENDS

Final calculation:
Peak: 8050 (highest HIGH after new high)
Trough: 7950 (lowest LOW before dropping below 8000)
Pullback: 8050 - 7950 = 100 points (1.24%)
""")

print("=== KEY DATA POINTS USED ===")
print("""
- NEW HIGH: Daily HIGH price that exceeds all previous highs
- PEAK: Highest HIGH price reached after the new high
- TROUGH: Lowest LOW price reached between peak and cycle end
- CYCLE END: When daily LOW drops below the original new high

Important notes:
1. Using INTRADAY data (High/Low), not just closing prices
2. Each trading day has: Open, High, Low, Close
3. Pullbacks measured from intraday peak to intraday trough
4. This captures the full range of price movement within each day
""")


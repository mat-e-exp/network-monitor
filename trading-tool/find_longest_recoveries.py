import csv
from datetime import datetime

# Read the CSV data
data = []
with open('ftse100.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # Skip header
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

# Find all multi-day trades and their recovery times
all_trades = []

for i, day in enumerate(data):
    if day['low'] < day['open'] * 0.99:  # Low is 1%+ below open
        buy_price = day['open'] * 0.99  # Buy at 1% below open
        target_price = buy_price + 50
        
        # Look forward to find when target is hit (starting from NEXT day)
        days_to_target = None
        for j in range(i + 1, min(i + 365, len(data))):  # Look up to 1 year ahead
            if data[j]['high'] >= target_price:
                days_to_target = j - i
                break
        
        if days_to_target is not None and days_to_target > 0:
            all_trades.append({
                'date': day['date'],
                'buy_price': buy_price,
                'target_price': target_price,
                'days_to_target': days_to_target,
                'buy_close': day['close']
            })

# Sort by days to target (longest first)
longest_recoveries = sorted(all_trades, key=lambda x: x['days_to_target'], reverse=True)

print(f"=== TOP 25 LONGEST RECOVERY TIMES ===")
print("Date\t\t\tBuy Price\tDays\tContext")
print("-" * 70)

for i, trade in enumerate(longest_recoveries[:25]):
    year = int(trade['date'].split('/')[-1].split()[0])
    
    # Add context based on year
    context = ""
    if year == 1987:
        context = "Black Monday crash"
    elif year in [1990, 1991]:
        context = "Gulf War recession"
    elif year in [2000, 2001, 2002]:
        context = "Dot-com crash"
    elif year == 2008:
        context = "Financial crisis"
    elif year in [2009, 2010]:
        context = "Post-crisis recovery"
    elif year == 2011:
        context = "European debt crisis"
    elif year == 2020:
        context = "COVID-19 pandemic"
    elif year in [2022, 2023]:
        context = "Inflation/interest rate concerns"
    
    print(f"{trade['date']:<20}\t{trade['buy_price']:.1f}\t\t{trade['days_to_target']}\t{context}")

# Show distribution of long recovery times
print(f"\n=== LONG RECOVERY ANALYSIS ===")
very_long = [t for t in all_trades if t['days_to_target'] > 100]
long = [t for t in all_trades if t['days_to_target'] > 60]
medium_long = [t for t in all_trades if t['days_to_target'] > 30]

print(f"Trades taking >30 days: {len(medium_long)} ({len(medium_long)/len(all_trades)*100:.1f}%)")
print(f"Trades taking >60 days: {len(long)} ({len(long)/len(all_trades)*100:.1f}%)")
print(f"Trades taking >100 days: {len(very_long)} ({len(very_long)/len(all_trades)*100:.1f}%)")

if very_long:
    avg_very_long = sum(t['days_to_target'] for t in very_long) / len(very_long)
    print(f"Average recovery time for >100 day trades: {avg_very_long:.1f} days")

# Show worst by decade
print(f"\n=== WORST CASE BY DECADE ===")
decades = {}
for trade in all_trades:
    year = int(trade['date'].split('/')[-1].split()[0])
    decade = (year // 10) * 10
    if decade not in decades:
        decades[decade] = []
    decades[decade].append(trade)

for decade in sorted(decades.keys()):
    worst = max(decades[decade], key=lambda x: x['days_to_target'])
    print(f"{decade}s worst: {worst['days_to_target']} days on {worst['date']} (buy at {worst['buy_price']:.1f})")

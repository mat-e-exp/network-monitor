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

print(f"Loaded {len(data)} trading days")

# Find days where low is 1%+ below open and simulate trades
all_trades = []
multi_day_trades = []

for i, day in enumerate(data):
    if day['low'] < day['open'] * 0.99:  # Low is 1%+ below open
        buy_price = day['open'] * 0.99  # Buy at 1% below open
        target_price = buy_price + 50
        
        # Look forward to find when target is hit (starting from NEXT day)
        days_to_target = None
        for j in range(i + 1, min(i + 252, len(data))):  # Start from next day, look up to 1 year ahead
            if data[j]['high'] >= target_price:
                days_to_target = j - i
                break
        
        trade = {
            'date': day['date'],
            'buy_price': buy_price,
            'target_price': target_price,
            'days_to_target': days_to_target
        }
        
        all_trades.append(trade)
        
        # Only include trades that take more than same day
        if days_to_target is not None and days_to_target > 0:
            multi_day_trades.append(trade)

# Analyze results (excluding same-day hits)
successful_multi_day = [t for t in multi_day_trades if t['days_to_target'] is not None]
failed_trades = [t for t in all_trades if t['days_to_target'] is None]

print(f"\n=== STRATEGY ANALYSIS (EXCLUDING SAME-DAY HITS) ===")
print(f"Total dip opportunities: {len(all_trades)}")
print(f"Same-day target hits (excluded): {len(all_trades) - len(multi_day_trades) - len(failed_trades)}")
print(f"Multi-day trades: {len(multi_day_trades)}")
print(f"Failed trades (never hit target): {len(failed_trades)}")
print(f"Multi-day success rate: {len(successful_multi_day)/len(multi_day_trades)*100:.1f}%" if multi_day_trades else "N/A")

if successful_multi_day:
    avg_days = sum(t['days_to_target'] for t in successful_multi_day) / len(successful_multi_day)
    print(f"Average days to +50 target (multi-day only): {avg_days:.1f} days")
    print(f"Average weeks to +50 target (multi-day only): {avg_days/7:.1f} weeks")
    
    # Show distribution for multi-day trades
    quick_wins = [t for t in successful_multi_day if t['days_to_target'] <= 5]
    fast_wins = [t for t in successful_multi_day if t['days_to_target'] <= 20]
    slow_wins = [t for t in successful_multi_day if t['days_to_target'] > 60]
    
    print(f"\nDistribution (multi-day trades only):")
    print(f"Hit target within 5 days: {len(quick_wins)} ({len(quick_wins)/len(successful_multi_day)*100:.1f}%)")
    print(f"Hit target within 20 days: {len(fast_wins)} ({len(fast_wins)/len(successful_multi_day)*100:.1f}%)")
    print(f"Took over 60 days: {len(slow_wins)} ({len(slow_wins)/len(successful_multi_day)*100:.1f}%)")
    
    # Median calculation
    days_list = sorted([t['days_to_target'] for t in successful_multi_day])
    median_days = days_list[len(days_list)//2]
    print(f"Median days to target: {median_days}")

# Show breakdown by decade
print(f"\n=== BREAKDOWN BY DECADE ===")
decades = {}
for trade in successful_multi_day:
    year = int(trade['date'].split('/')[-1].split()[0])
    decade = (year // 10) * 10
    if decade not in decades:
        decades[decade] = []
    decades[decade].append(trade['days_to_target'])

for decade in sorted(decades.keys()):
    avg = sum(decades[decade]) / len(decades[decade])
    print(f"{decade}s: {len(decades[decade])} trades, avg {avg:.1f} days")

# Show some recent examples
print(f"\n=== RECENT MULTI-DAY EXAMPLES ===")
recent_multi_day = [t for t in multi_day_trades if ('2023' in t['date'] or '2024' in t['date'] or '2025' in t['date']) and t['days_to_target'] is not None][-15:]
for trade in recent_multi_day:
    print(f"{trade['date']}: Buy at {trade['buy_price']:.1f}, Target {trade['target_price']:.1f}, Days: {trade['days_to_target']}")

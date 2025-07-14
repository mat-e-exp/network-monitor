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
trades = []
for i, day in enumerate(data):
    if day['low'] < day['open'] * 0.99:  # Low is 1%+ below open
        buy_price = day['open'] * 0.99  # Buy at 1% below open
        target_price = buy_price + 50
        
        # Look forward to find when target is hit
        days_to_target = None
        for j in range(i, min(i + 252, len(data))):  # Look up to 1 year ahead
            if data[j]['high'] >= target_price:
                days_to_target = j - i
                break
        
        trades.append({
            'date': day['date'],
            'buy_price': buy_price,
            'target_price': target_price,
            'days_to_target': days_to_target
        })

# Analyze results
successful_trades = [t for t in trades if t['days_to_target'] is not None]
failed_trades = [t for t in trades if t['days_to_target'] is None]

print(f"\n=== STRATEGY ANALYSIS ===")
print(f"Total trades: {len(trades)}")
print(f"Successful trades (hit +50 within 1 year): {len(successful_trades)}")
print(f"Failed trades (didn't hit +50 within 1 year): {len(failed_trades)}")
print(f"Success rate: {len(successful_trades)/len(trades)*100:.1f}%")

if successful_trades:
    avg_days = sum(t['days_to_target'] for t in successful_trades) / len(successful_trades)
    print(f"Average days to +50 target: {avg_days:.1f} days")
    print(f"Average weeks to +50 target: {avg_days/7:.1f} weeks")
    
    # Show distribution
    quick_wins = [t for t in successful_trades if t['days_to_target'] <= 5]
    fast_wins = [t for t in successful_trades if t['days_to_target'] <= 20]
    slow_wins = [t for t in successful_trades if t['days_to_target'] > 60]
    
    print(f"\nDistribution:")
    print(f"Hit target within 5 days: {len(quick_wins)} ({len(quick_wins)/len(successful_trades)*100:.1f}%)")
    print(f"Hit target within 20 days: {len(fast_wins)} ({len(fast_wins)/len(successful_trades)*100:.1f}%)")
    print(f"Took over 60 days: {len(slow_wins)} ({len(slow_wins)/len(successful_trades)*100:.1f}%)")

# Show some recent examples
print(f"\n=== RECENT EXAMPLES ===")
recent_trades = [t for t in trades if '2024' in t['date'] or '2025' in t['date']][-10:]
for trade in recent_trades:
    days = trade['days_to_target'] if trade['days_to_target'] is not None else '>252'
    print(f"{trade['date']}: Buy at {trade['buy_price']:.1f}, Target {trade['target_price']:.1f}, Days: {days}")

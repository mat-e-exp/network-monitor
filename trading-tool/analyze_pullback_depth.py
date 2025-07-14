import csv

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

# Find new highs and track pullback depth
new_high_cycles = []
running_high = 0

for i, day in enumerate(data):
    current_high = day['high']
    
    # Check if this is a new all-time high
    if current_high > running_high:
        # This is a new high
        new_high_date = day['date']
        new_high_value = current_high
        running_high = current_high
        
        # Look forward to find:
        # 1. The peak reached after this new high
        # 2. The deepest pullback from the peak
        peak_value = new_high_value
        peak_date = new_high_date
        deepest_low = new_high_value
        deepest_low_date = new_high_date
        dropped_below_original = False
        days_to_drop_below = None
        
        for j in range(i + 1, len(data)):
            future_day = data[j]
            
            # Track the peak
            if future_day['high'] > peak_value:
                peak_value = future_day['high']
                peak_date = future_day['date']
                running_high = peak_value
            
            # Track the deepest low from the peak
            if future_day['low'] < deepest_low:
                deepest_low = future_day['low']
                deepest_low_date = future_day['date']
            
            # Check if it dropped below the original new high (end of cycle)
            if future_day['low'] < new_high_value and not dropped_below_original:
                dropped_below_original = True
                days_to_drop_below = j - i
                break
        
        # Calculate pullback metrics
        peak_to_trough = peak_value - deepest_low
        peak_to_trough_percent = (peak_to_trough / peak_value) * 100
        new_high_to_trough = new_high_value - deepest_low
        new_high_to_trough_percent = (new_high_to_trough / new_high_value) * 100
        
        cycle = {
            'new_high_date': new_high_date,
            'new_high_value': new_high_value,
            'peak_date': peak_date,
            'peak_value': peak_value,
            'deepest_low': deepest_low,
            'deepest_low_date': deepest_low_date,
            'peak_to_trough_points': peak_to_trough,
            'peak_to_trough_percent': peak_to_trough_percent,
            'new_high_to_trough_points': new_high_to_trough,
            'new_high_to_trough_percent': new_high_to_trough_percent,
            'days_to_drop_below': days_to_drop_below,
            'dropped_below_original': dropped_below_original
        }
        
        new_high_cycles.append(cycle)

# Filter meaningful cycles (where we have a complete cycle)
complete_cycles = [c for c in new_high_cycles if c['dropped_below_original']]

print(f"\n=== PULLBACK DEPTH ANALYSIS ===")
print(f"Complete new high cycles: {len(complete_cycles)}")

if complete_cycles:
    # 100+ point pullback analysis
    pullbacks_100_plus = [c for c in complete_cycles if c['peak_to_trough_points'] >= 100]
    pullbacks_from_new_high_100_plus = [c for c in complete_cycles if c['new_high_to_trough_points'] >= 100]
    
    print(f"\nPullbacks of 100+ points from peak: {len(pullbacks_100_plus)} ({len(pullbacks_100_plus)/len(complete_cycles)*100:.1f}%)")
    print(f"Pullbacks of 100+ points from new high: {len(pullbacks_from_new_high_100_plus)} ({len(pullbacks_from_new_high_100_plus)/len(complete_cycles)*100:.1f}%)")
    
    # Distribution by pullback size from peak
    small_pullbacks = [c for c in complete_cycles if c['peak_to_trough_points'] < 50]
    medium_pullbacks = [c for c in complete_cycles if 50 <= c['peak_to_trough_points'] < 100]
    large_pullbacks = [c for c in complete_cycles if 100 <= c['peak_to_trough_points'] < 200]
    huge_pullbacks = [c for c in complete_cycles if c['peak_to_trough_points'] >= 200]
    
    print(f"\nPullback distribution from peak:")
    print(f"Small (<50 points): {len(small_pullbacks)} ({len(small_pullbacks)/len(complete_cycles)*100:.1f}%)")
    print(f"Medium (50-99 points): {len(medium_pullbacks)} ({len(medium_pullbacks)/len(complete_cycles)*100:.1f}%)")
    print(f"Large (100-199 points): {len(large_pullbacks)} ({len(large_pullbacks)/len(complete_cycles)*100:.1f}%)")
    print(f"Huge (200+ points): {len(huge_pullbacks)} ({len(huge_pullbacks)/len(complete_cycles)*100:.1f}%)")
    
    # Average pullback stats
    avg_pullback_points = sum(c['peak_to_trough_points'] for c in complete_cycles) / len(complete_cycles)
    avg_pullback_percent = sum(c['peak_to_trough_percent'] for c in complete_cycles) / len(complete_cycles)
    
    pullback_points = [c['peak_to_trough_points'] for c in complete_cycles]
    pullback_points.sort()
    median_pullback = pullback_points[len(pullback_points)//2]
    
    print(f"\nAverage pullback from peak: {avg_pullback_points:.1f} points ({avg_pullback_percent:.2f}%)")
    print(f"Median pullback from peak: {median_pullback:.1f} points")
    print(f"Largest pullback: {max(pullback_points):.1f} points")

# Show the biggest pullbacks
print(f"\n=== TOP 15 BIGGEST PULLBACKS AFTER NEW HIGHS ===")
biggest_pullbacks = sorted(complete_cycles, key=lambda x: x['peak_to_trough_points'], reverse=True)[:15]

print("New High Date\t\tPeak\t\tTrough\t\tPullback\tPullback%")
print("-" * 85)
for cycle in biggest_pullbacks:
    print(f"{cycle['new_high_date']:<20}\t{cycle['peak_value']:.1f}\t\t{cycle['deepest_low']:.1f}\t\t{cycle['peak_to_trough_points']:.1f}\t\t{cycle['peak_to_trough_percent']:.2f}%")

# Recent pullbacks
print(f"\n=== RECENT PULLBACKS (2020+) ===")
recent_cycles = [c for c in complete_cycles if any(year in c['new_high_date'] for year in ['2020', '2021', '2022', '2023', '2024', '2025'])]

print("New High Date\t\tPeak\t\tTrough\t\tPullback\tPullback%")
print("-" * 85)
for cycle in recent_cycles:
    print(f"{cycle['new_high_date']:<20}\t{cycle['peak_value']:.1f}\t\t{cycle['deepest_low']:.1f}\t\t{cycle['peak_to_trough_points']:.1f}\t\t{cycle['peak_to_trough_percent']:.2f}%")

# Specific 100+ point analysis
print(f"\n=== ALL PULLBACKS OF 100+ POINTS ===")
print("New High Date\t\tPeak\t\tTrough\t\tPullback\tPullback%\tContext")
print("-" * 100)
for cycle in pullbacks_100_plus:
    year = int(cycle['new_high_date'].split('/')[-1].split()[0])
    context = ""
    if year == 1987:
        context = "Black Monday"
    elif year in [2000, 2001, 2002]:
        context = "Dot-com crash"
    elif year == 2008:
        context = "Financial crisis"
    elif year == 2020:
        context = "COVID-19"
    elif year in [2022, 2023]:
        context = "Inflation concerns"
    
    print(f"{cycle['new_high_date']:<20}\t{cycle['peak_value']:.1f}\t\t{cycle['deepest_low']:.1f}\t\t{cycle['peak_to_trough_points']:.1f}\t\t{cycle['peak_to_trough_percent']:.2f}%\t\t{context}")


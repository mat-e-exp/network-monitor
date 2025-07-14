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

# Find new highs and track how much higher they go
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
        # 2. When it drops back below this new high level
        peak_value = new_high_value
        peak_date = new_high_date
        dropped_below = False
        days_to_drop = None
        
        for j in range(i + 1, len(data)):
            future_day = data[j]
            
            # Track the peak
            if future_day['high'] > peak_value:
                peak_value = future_day['high']
                peak_date = future_day['date']
                running_high = peak_value
            
            # Check if it dropped below the original new high
            if future_day['low'] < new_high_value and not dropped_below:
                dropped_below = True
                days_to_drop = j - i
                break
        
        # Calculate the advance from new high to peak
        advance_points = peak_value - new_high_value
        advance_percent = (advance_points / new_high_value) * 100
        
        cycle = {
            'new_high_date': new_high_date,
            'new_high_value': new_high_value,
            'peak_date': peak_date,
            'peak_value': peak_value,
            'advance_points': advance_points,
            'advance_percent': advance_percent,
            'days_to_drop': days_to_drop,
            'dropped_below': dropped_below
        }
        
        new_high_cycles.append(cycle)

# Filter out cycles where advance is 0 (same day peaks)
meaningful_cycles = [c for c in new_high_cycles if c['advance_points'] > 0]

print(f"\n=== NEW HIGH ANALYSIS ===")
print(f"Total new highs identified: {len(new_high_cycles)}")
print(f"Cycles with meaningful advance: {len(meaningful_cycles)}")

if meaningful_cycles:
    # Calculate statistics
    avg_advance_points = sum(c['advance_points'] for c in meaningful_cycles) / len(meaningful_cycles)
    avg_advance_percent = sum(c['advance_percent'] for c in meaningful_cycles) / len(meaningful_cycles)
    
    advances_points = [c['advance_points'] for c in meaningful_cycles]
    advances_percent = [c['advance_percent'] for c in meaningful_cycles]
    
    advances_points.sort()
    advances_percent.sort()
    
    median_points = advances_points[len(advances_points)//2]
    median_percent = advances_percent[len(advances_percent)//2]
    
    print(f"\nAverage advance after new high: {avg_advance_points:.1f} points ({avg_advance_percent:.2f}%)")
    print(f"Median advance after new high: {median_points:.1f} points ({median_percent:.2f}%)")
    print(f"Max advance: {max(advances_points):.1f} points ({max(advances_percent):.2f}%)")
    print(f"Min advance: {min(advances_points):.1f} points ({min(advances_percent):.2f}%)")
    
    # Distribution analysis
    small_advances = [c for c in meaningful_cycles if c['advance_percent'] < 1]
    medium_advances = [c for c in meaningful_cycles if 1 <= c['advance_percent'] < 5]
    large_advances = [c for c in meaningful_cycles if c['advance_percent'] >= 5]
    
    print(f"\nDistribution:")
    print(f"Small advances (<1%): {len(small_advances)} ({len(small_advances)/len(meaningful_cycles)*100:.1f}%)")
    print(f"Medium advances (1-5%): {len(medium_advances)} ({len(medium_advances)/len(meaningful_cycles)*100:.1f}%)")
    print(f"Large advances (>5%): {len(large_advances)} ({len(large_advances)/len(meaningful_cycles)*100:.1f}%)")
    
    # Show cycles that dropped below
    dropped_cycles = [c for c in meaningful_cycles if c['dropped_below']]
    never_dropped = [c for c in meaningful_cycles if not c['dropped_below']]
    
    print(f"\nRetracement analysis:")
    print(f"Cycles that eventually dropped below new high: {len(dropped_cycles)} ({len(dropped_cycles)/len(meaningful_cycles)*100:.1f}%)")
    print(f"Cycles that never dropped below: {len(never_dropped)} ({len(never_dropped)/len(meaningful_cycles)*100:.1f}%)")
    
    if dropped_cycles:
        avg_days_to_drop = sum(c['days_to_drop'] for c in dropped_cycles) / len(dropped_cycles)
        print(f"Average days before dropping below new high: {avg_days_to_drop:.1f}")

# Show the biggest advances
print(f"\n=== TOP 20 BIGGEST ADVANCES AFTER NEW HIGHS ===")
biggest_advances = sorted(meaningful_cycles, key=lambda x: x['advance_percent'], reverse=True)[:20]

print("New High Date\t\tNew High\tPeak\t\tAdvance\tAdvance%")
print("-" * 80)
for cycle in biggest_advances:
    print(f"{cycle['new_high_date']:<20}\t{cycle['new_high_value']:.1f}\t\t{cycle['peak_value']:.1f}\t\t{cycle['advance_points']:.1f}\t{cycle['advance_percent']:.2f}%")

# Show recent cycles
print(f"\n=== RECENT NEW HIGH CYCLES (2020+) ===")
recent_cycles = [c for c in meaningful_cycles if '2020' in c['new_high_date'] or '2021' in c['new_high_date'] or '2022' in c['new_high_date'] or '2023' in c['new_high_date'] or '2024' in c['new_high_date'] or '2025' in c['new_high_date']]

print("New High Date\t\tNew High\tPeak\t\tAdvance\tAdvance%\tDropped Below")
print("-" * 90)
for cycle in recent_cycles[-15:]:  # Last 15 recent cycles
    dropped = "Yes" if cycle['dropped_below'] else "No"
    print(f"{cycle['new_high_date']:<20}\t{cycle['new_high_value']:.1f}\t\t{cycle['peak_value']:.1f}\t\t{cycle['advance_points']:.1f}\t{cycle['advance_percent']:.2f}%\t\t{dropped}")


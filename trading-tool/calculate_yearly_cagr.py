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
                    'open': float(row[1]),
                    'high': float(row[2]),
                    'low': float(row[3]),
                    'close': float(row[4])
                })
            except ValueError:
                continue

print(f"Loaded {len(data)} trading days")

# Group data by year and calculate yearly returns
yearly_data = {}

for record in data:
    # Extract year from date (format: M/D/YYYY HH:MM:SS)
    try:
        date_part = record['date'].split()[0]  # Get date part before time
        month, day, year = date_part.split('/')
        year = int(year)
        
        if year not in yearly_data:
            yearly_data[year] = []
        yearly_data[year].append(record)
    except (ValueError, IndexError):
        continue

# Calculate yearly returns (using first and last trading day of each year)
yearly_returns = []

for year in sorted(yearly_data.keys()):
    year_records = yearly_data[year]
    if len(year_records) >= 2:  # Need at least 2 records
        start_price = year_records[0]['close']
        end_price = year_records[-1]['close']
        
        # Calculate annual return
        annual_return = ((end_price - start_price) / start_price) * 100
        
        yearly_returns.append({
            'year': year,
            'start_price': start_price,
            'end_price': end_price,
            'annual_return': annual_return,
            'trading_days': len(year_records)
        })

print(f"\n=== YEARLY RETURNS (CAGR) ===")
print("Year\tStart\tEnd\tReturn%\tTrading Days")
print("-" * 50)

total_return_sum = 0
positive_years = 0
negative_years = 0
best_year = None
worst_year = None

for year_data in yearly_returns:
    year = year_data['year']
    start = year_data['start_price']
    end = year_data['end_price']
    return_pct = year_data['annual_return']
    days = year_data['trading_days']
    
    print(f"{year}\t{start:.1f}\t{end:.1f}\t{return_pct:+.2f}%\t{days}")
    
    total_return_sum += return_pct
    
    if return_pct > 0:
        positive_years += 1
    else:
        negative_years += 1
    
    if best_year is None or return_pct > best_year['return']:
        best_year = {'year': year, 'return': return_pct}
    
    if worst_year is None or return_pct < worst_year['return']:
        worst_year = {'year': year, 'return': return_pct}

# Calculate overall statistics
total_years = len(yearly_returns)
average_annual_return = total_return_sum / total_years if total_years > 0 else 0

# Calculate compound annual growth rate for entire period
if yearly_returns:
    first_year = yearly_returns[0]
    last_year = yearly_returns[-1]
    
    start_value = first_year['start_price']
    end_value = last_year['end_price']
    years = last_year['year'] - first_year['year'] + 1
    
    # CAGR = (End Value / Start Value)^(1/years) - 1
    overall_cagr = (pow(end_value / start_value, 1/years) - 1) * 100

print(f"\n=== SUMMARY STATISTICS ===")
print(f"Total years analyzed: {total_years}")
print(f"Positive years: {positive_years} ({positive_years/total_years*100:.1f}%)")
print(f"Negative years: {negative_years} ({negative_years/total_years*100:.1f}%)")
print(f"Average annual return: {average_annual_return:.2f}%")
print(f"Best year: {best_year['year']} (+{best_year['return']:.2f}%)")
print(f"Worst year: {worst_year['year']} ({worst_year['return']:.2f}%)")
print(f"Overall CAGR ({first_year['year']}-{last_year['year']}): {overall_cagr:.2f}%")

# Calculate decade averages
print(f"\n=== DECADE AVERAGES ===")
decades = {}
for year_data in yearly_returns:
    decade = (year_data['year'] // 10) * 10
    if decade not in decades:
        decades[decade] = []
    decades[decade].append(year_data['annual_return'])

for decade in sorted(decades.keys()):
    decade_returns = decades[decade]
    decade_avg = sum(decade_returns) / len(decade_returns)
    decade_positive = sum(1 for r in decade_returns if r > 0)
    decade_negative = len(decade_returns) - decade_positive
    
    print(f"{decade}s: {decade_avg:+.2f}% avg ({decade_positive} positive, {decade_negative} negative years)")

# Show distribution of returns
print(f"\n=== RETURN DISTRIBUTION ===")
returns_list = [y['annual_return'] for y in yearly_returns]
returns_list.sort()

large_gains = [r for r in returns_list if r > 20]
good_gains = [r for r in returns_list if 10 <= r <= 20]
modest_gains = [r for r in returns_list if 0 < r < 10]
modest_losses = [r for r in returns_list if -10 < r <= 0]
large_losses = [r for r in returns_list if r <= -10]

print(f"Large gains (>20%): {len(large_gains)} years")
print(f"Good gains (10-20%): {len(good_gains)} years")
print(f"Modest gains (0-10%): {len(modest_gains)} years")
print(f"Modest losses (0 to -10%): {len(modest_losses)} years")
print(f"Large losses (>-10%): {len(large_losses)} years")


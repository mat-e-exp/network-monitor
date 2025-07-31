#!/bin/bash

echo "=== Live Internet Connections on $(hostname) ==="
echo "Generated on: $(date)"
echo ""

echo "Active Network Connections:"
echo "=========================="

# Get active connections with process info
lsof -i -n -P | grep -E "(ESTABLISHED|LISTEN)" | while read line; do
    # Parse the lsof output
    command=$(echo "$line" | awk '{print $1}')
    pid=$(echo "$line" | awk '{print $2}')
    user=$(echo "$line" | awk '{print $3}')
    fd=$(echo "$line" | awk '{print $4}')
    type=$(echo "$line" | awk '{print $5}')
    node=$(echo "$line" | awk '{print $9}')
    state=$(echo "$line" | awk '{print $10}')
    
    # Skip if it's a local connection only (localhost/127.0.0.1)
    if [[ "$node" =~ ^127\.|localhost ]]; then
        continue
    fi
    
    # Format and display the connection
    printf "%-20s %-8s %-12s %-35s %s\n" "$command" "$pid" "$user" "$node" "$state"
done | sort -k1

echo ""
echo "Connection Summary by Application:"
echo "================================="

# Count connections per application
lsof -i -n -P | grep -E "(ESTABLISHED|LISTEN)" | grep -v -E "127\.|localhost" | awk '{print $1}' | sort | uniq -c | sort -nr | while read count app; do
    printf "%-20s %s connections\n" "$app" "$count"
done

echo ""
echo "Network Interface Status:"
echo "========================"
ifconfig | grep -A1 "flags.*UP" | grep "inet " | while read line; do
    interface=$(echo "$line" | awk '{print $1}' | sed 's/://')
    ip=$(echo "$line" | awk '{print $2}')
    echo "Interface: $interface - IP: $ip"
done

echo ""
echo "DNS Servers in use:"
echo "=================="
scutil --dns | grep "nameserver" | sort -u
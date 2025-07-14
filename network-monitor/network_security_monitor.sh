#!/bin/bash

echo "=========================================="
echo "   NETWORK SECURITY MONITORING TOOL"
echo "=========================================="
echo "Generated on: $(date)"
echo "Host: $(hostname)"
echo ""

# =============================================================================
# PART 1: NETWORK CONNECTIONS ANALYSIS
# =============================================================================

echo "=== ACTIVE NETWORK CONNECTIONS ==="
echo ""

echo "Live Internet Connections:"
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

echo ""
echo ""

# =============================================================================
# PART 2: SECURITY RISK ANALYSIS
# =============================================================================

echo "=== SECURITY RISK ANALYSIS ==="
echo ""

# Function to classify risk level
classify_risk() {
    local app="$1"
    local connection="$2"
    local count="$3"
    
    # High risk indicators
    if [[ "$app" == "PowerChim"* ]] && [[ "$count" -gt 10 ]]; then
        echo "HIGH - Excessive connections ($count) - possible malware"
    elif [[ "$connection" =~ "fe80:" ]] && [[ "$app" == "rapportd" ]] && [[ ! "$connection" =~ "127\.|localhost" ]]; then
        echo "HIGH - External IPv6 connection from system service"
    elif [[ "$app" =~ ^[a-f0-9]{8}$ ]]; then
        echo "HIGH - Suspicious process name (random hex)"
    elif [[ "$connection" =~ ":22[0-9][0-9]|:23[0-9][0-9]" ]]; then
        echo "MEDIUM - Non-standard high port usage"
    elif [[ "$app" == "Python" ]] && [[ "$connection" =~ "LISTEN" ]] && [[ ! "$connection" =~ "127\.|localhost" ]]; then
        echo "MEDIUM - Python server listening externally"
    elif [[ "$app" =~ "VPN|Nord" ]]; then
        echo "LOW - VPN traffic (verify legitimacy)"
    elif [[ "$app" =~ "Google|Chrome|Safari|Firefox" ]]; then
        echo "LOW - Browser traffic"
    elif [[ "$app" =~ "node|npm" ]]; then
        echo "LOW - Development tools"
    elif [[ "$connection" =~ "443|80" ]]; then
        echo "LOW - Standard web traffic"
    else
        echo "MEDIUM - Requires investigation"
    fi
}

echo "APPLICATION RISK ASSESSMENT:"
echo "============================"

# Analyze each application
lsof -i -n -P | grep -E "(ESTABLISHED|LISTEN)" | grep -v -E "127\.|localhost" | awk '{print $1}' | sort | uniq -c | sort -nr | while read count app; do
    # Get a sample connection for this app
    sample_connection=$(lsof -i -n -P | grep -E "(ESTABLISHED|LISTEN)" | grep "$app" | grep -v -E "127\.|localhost" | head -1 | awk '{print $9 " " $10}')
    
    risk_level=$(classify_risk "$app" "$sample_connection" "$count")
    
    printf "%-20s %-8s %s\n" "$app" "$count" "$risk_level"
done

echo ""
echo "DETAILED THREAT ANALYSIS:"
echo "========================="

# PowerChimes analysis
powerchim_count=$(lsof -i -n -P | grep "PowerChim" | grep -E "(ESTABLISHED|LISTEN)" | grep -v -E "127\.|localhost" | wc -l)
if [[ "$powerchim_count" -gt 0 ]]; then
    echo "🚨 CRITICAL ALERT: PowerChimes"
    echo "   Connections: $powerchim_count"
    echo "   Risk Level: HIGH - Potential malware activity"
    echo "   Process ID: $(lsof -i -n -P | grep "PowerChim" | head -1 | awk '{print $2}')"
    echo "   Action Required: Immediate investigation"
    echo ""
fi

# Check for other high-risk patterns
suspicious_apps=$(lsof -i -n -P | grep -E "(ESTABLISHED|LISTEN)" | grep -v -E "127\.|localhost|Google|Chrome|Safari|node|Python|Nord|Control" | awk '{print $1}' | sort | uniq)
if [[ -n "$suspicious_apps" ]]; then
    echo "⚠️  Unusual Applications with Network Access:"
    echo "$suspicious_apps" | while read app; do
        count=$(lsof -i -n -P | grep "$app" | grep -E "(ESTABLISHED|LISTEN)" | grep -v -E "127\.|localhost" | wc -l)
        echo "   - $app: $count connections"
    done
    echo ""
fi

echo "EXPOSED SERVICES (Listening Ports):"
echo "===================================="
lsof -i -n -P | grep "LISTEN" | grep -v -E "127\.|localhost" | while read line; do
    app=$(echo "$line" | awk '{print $1}')
    port=$(echo "$line" | awk '{print $9}' | cut -d: -f2)
    
    if [[ "$port" -lt 1024 ]]; then
        risk="HIGH - Privileged port"
    elif [[ "$port" =~ ^(8000|3000|4000|5000|8080)$ ]]; then
        risk="MEDIUM - Development port exposed"
    else
        risk="LOW - Standard service port"
    fi
    
    printf "%-20s Port %-8s %s\n" "$app" "$port" "$risk"
done

echo ""
echo "=========================================="
echo "SECURITY RECOMMENDATIONS:"
echo "=========================================="

# Count high-risk items
high_risk_count=$(lsof -i -n -P | grep -E "(ESTABLISHED|LISTEN)" | grep -v -E "127\.|localhost" | awk '{print $1}' | sort | uniq -c | awk '$1 > 10 {count++} END {print count+0}')

if [[ "$powerchim_count" -gt 0 ]]; then
    echo "🚨 IMMEDIATE ACTIONS REQUIRED:"
    echo "1. Terminate PowerChimes process (PID: $(lsof -i -n -P | grep "PowerChim" | head -1 | awk '{print $2}'))"
    echo "2. Run comprehensive malware scan"
    echo "3. Check system for unauthorized software"
    echo ""
fi

echo "📋 GENERAL RECOMMENDATIONS:"
echo "1. Monitor applications with excessive connections"
echo "2. Verify legitimacy of all VPN software"
echo "3. Secure development servers (consider localhost-only binding)"
echo "4. Review firewall rules for exposed services"
echo "5. Regular security scans recommended"
echo ""

echo "📊 SUMMARY:"
total_apps=$(lsof -i -n -P | grep -E "(ESTABLISHED|LISTEN)" | grep -v -E "127\.|localhost" | awk '{print $1}' | sort | uniq | wc -l)
total_connections=$(lsof -i -n -P | grep -E "(ESTABLISHED|LISTEN)" | grep -v -E "127\.|localhost" | wc -l)
echo "Total applications with internet access: $total_apps"
echo "Total active connections: $total_connections"
if [[ "$powerchim_count" -gt 0 ]]; then
    echo "Security Status: 🚨 HIGH RISK - Immediate attention required"
else
    echo "Security Status: ⚠️  Monitoring recommended"
fi

echo ""
echo "Scan completed at: $(date)"
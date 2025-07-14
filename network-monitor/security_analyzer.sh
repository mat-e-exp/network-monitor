#!/bin/bash

echo "=== Network Security Analysis ==="
echo "Generated on: $(date)"
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

echo "SECURITY RISK ASSESSMENT:"
echo "========================="

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
    echo "⚠️  PowerChimes: $powerchim_count connections detected"
    echo "   - This is highly unusual for this application"
    echo "   - Recommend: Check Activity Monitor, scan for malware"
    echo "   - Process ID: $(lsof -i -n -P | grep "PowerChim" | head -1 | awk '{print $2}')"
    echo ""
fi

# Check for suspicious listening ports
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
echo "RECOMMENDATIONS:"
echo "================"
echo "1. Investigate PowerChimes excessive connections immediately"
echo "2. Verify NordVPN legitimacy and check for license/subscription"
echo "3. Consider firewall rules for development servers (Python:8000)"
echo "4. Monitor rapportd for unusual external connections"
echo "5. Regular malware scans recommended"
# Network Monitor

Experiements whilst trying to understand live network connections.

## Scripts

### 1. network_connections.sh
A basic network connection monitoring script that displays:
- Active internet connections (excluding localhost)
- Connection summary by application
- Network interface status
- DNS servers in use

**Usage:** `./network_connections.sh`

### 2. network_security_monitor.sh
A comprehensive security-focused network monitoring tool that provides:
- **Network Connections Analysis**: Active connections with process details
- **Security Risk Analysis**: Risk classification for each application
- **Threat Detection**: Specific checks for suspicious activity (PowerChimes malware detection)
- **Exposed Services**: Analysis of listening ports and their security implications
- **Security Recommendations**: Actionable advice based on findings

**Usage:** `./network_security_monitor.sh`

### 3. security_analyzer.sh
A focused security assessment tool that:
- Performs risk assessment of network-connected applications
- Detects potential threats and suspicious processes
- Analyzes exposed services and ports
- Provides targeted security recommendations

**Usage:** `./security_analyzer.sh`

## Requirements
- macOS (uses `lsof`, `ifconfig`, `scutil`)
- Bash shell
- Execute permissions: `chmod +x *.sh`

## Security Focus
These scripts are designed for **defensive security monitoring** to help identify:
- Unusual network activity
- Potential malware (specifically PowerChimes detection)
- Exposed services and ports
- Suspicious connection patterns
#!/usr/bin/env python3
"""
Check network configuration for OnlyOffice integration
"""

import socket
import requests

print("\n" + "="*70)
print("🔍 Network Configuration Check")
print("="*70)

# 1. Get local IP addresses
print("\n1️⃣ Local IP Addresses:")
try:
    hostname = socket.gethostname()
    print(f"   Hostname: {hostname}")
    
    # Method 1: Hostname IP
    try:
        hostname_ip = socket.gethostbyname(hostname)
        print(f"   Hostname IP: {hostname_ip}")
    except:
        print(f"   Hostname IP: Could not resolve")
    
    # Method 2: Connect to external (gets actual network IP)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        network_ip = s.getsockname()[0]
        s.close()
        print(f"   Network IP: {network_ip}")
    except:
        print(f"   Network IP: Could not determine")
    
    # Method 3: Check if host.docker.internal resolves
    try:
        docker_internal = socket.gethostbyname('host.docker.internal')
        print(f"   host.docker.internal: {docker_internal} ✅")
    except:
        print(f"   host.docker.internal: Not available ❌")
        
except Exception as e:
    print(f"   Error: {e}")

# 2. Check Flask backend
print("\n2️⃣ Flask Backend Status:")
try:
    response = requests.get('http://localhost:5000/api/health', timeout=2)
    if response.status_code == 200:
        print(f"   ✅ Flask is running on localhost:5000")
    else:
        print(f"   ⚠️  Flask returned status {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"   ❌ Flask is not running on localhost:5000")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. Check OnlyOffice
print("\n3️⃣ OnlyOffice Document Server Status:")
try:
    response = requests.get('http://localhost:8080/healthcheck', timeout=2)
    if response.status_code == 200:
        print(f"   ✅ OnlyOffice is running on localhost:8080")
    else:
        print(f"   ⚠️  OnlyOffice returned status {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"   ❌ OnlyOffice is not running on localhost:8080")
    print(f"   💡 Start it with: docker start onlyoffice-documentserver")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 4. Check if Flask is accessible from network IP
print("\n4️⃣ Flask Accessibility Test:")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    network_ip = s.getsockname()[0]
    s.close()
    
    print(f"   Testing Flask at http://{network_ip}:5000/api/health")
    try:
        response = requests.get(f'http://{network_ip}:5000/api/health', timeout=2)
        if response.status_code == 200:
            print(f"   ✅ Flask is accessible from network IP")
            print(f"   💡 OnlyOffice should use: http://{network_ip}:5000")
        else:
            print(f"   ⚠️  Flask returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Flask is NOT accessible from network IP")
        print(f"   💡 This might be a firewall issue")
        print(f"   💡 Try allowing port 5000 in Windows Firewall")
    except Exception as e:
        print(f"   ❌ Error: {e}")
except Exception as e:
    print(f"   ❌ Could not determine network IP: {e}")

# 5. Recommendations
print("\n" + "="*70)
print("📋 Recommendations:")
print("="*70)

try:
    # Check which method works
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    network_ip = s.getsockname()[0]
    s.close()
    
    print(f"\n✅ Best option: Use network IP")
    print(f"   Backend URL: http://{network_ip}:5000")
    print(f"\n📝 If OnlyOffice still can't connect:")
    print(f"   1. Check Windows Firewall")
    print(f"   2. Allow port 5000 for Python")
    print(f"   3. Restart OnlyOffice container:")
    print(f"      docker restart onlyoffice-documentserver")
    
except:
    try:
        docker_internal = socket.gethostbyname('host.docker.internal')
        print(f"\n✅ Best option: Use host.docker.internal")
        print(f"   Backend URL: http://host.docker.internal:5000")
    except:
        print(f"\n⚠️  Neither network IP nor host.docker.internal available")
        print(f"   This might require Docker network configuration")

print("\n" + "="*70 + "\n")

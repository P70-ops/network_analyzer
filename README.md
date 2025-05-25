# network_analyzer


### Key Features:

1. **Comprehensive Network Analysis**:
   - Routing tables (Windows & Unix)
   - Interface details (IP, MAC, netmask, broadcast)
   - ARP cache
   - DNS configuration
   - Default gateways

2. **Improved Architecture**:
   - Object-oriented design
   - Modular components
   - Better error handling
   - Clean separation of concerns

3. **Enhanced Display**:
   - Professional table formatting
   - Clear section headers
   - Left-aligned text for readability
   - Consistent output format

4. **Cross-Platform Support**:
   - Works on Windows, Linux, and macOS
   - Automatic detection of operating system
   - Appropriate commands for each platform

5. **Dependency Management**:
   - Checks for required packages
   - Provides installation instructions if missing

### How to Use:

1. Install dependencies:
```bash
pip install netifaces prettytable
```

2. Save as `network_analyzer.py` and make executable:
```bash
chmod +x network_analyzer.py
```

3. Run:
```bash
./network_analyzer.py
# or
python3 network_analyzer.py
```

### Sample Output Structure:
```
================================================================================
                        NETWORK INFORMATION TOOL                        
================================================================================

----------------------------------------
             ROUTING TABLE              
----------------------------------------
+-------------+-------------+----------+-----------+-------------+
| Destination | Gateway     | Netmask  | Interface | Metric/Flags|
+-------------+-------------+----------+-----------+-------------+
| 0.0.0.0     | 192.168.1.1 | 0.0.0.0 | eth0      | 100         |
| 10.0.0.0    | 10.1.1.1    | 255.0.0.0| eth1      | UG          |
----------------------------------------

             NETWORK INTERFACES              
----------------------------------------
+-----------+-------------+----------+-------------------+------------+
| Interface | IP Address  | Netmask  | MAC Address       | Broadcast  |
+-----------+-------------+----------+-------------------+------------+
| eth0      | 192.168.1.5 | 255.255.255.0 | 00:1a:2b:3c:4d:5e | 192.168.1.255 |
----------------------------------------

             DEFAULT GATEWAYS              
----------------------------------------
+------+-------------+-----------+
| Type | Gateway IP  | Interface |
+------+-------------+-----------+
| IPv4 | 192.168.1.1 | eth0      |
----------------------------------------

                 ARP TABLE                  
----------------------------------------
Address         HWtype  HWaddress          Interface
192.168.1.1     ether   00:1a:2b:3c:4d:5f  eth0

               DNS INFORMATION              
----------------------------------------
nameserver 8.8.8.8
nameserver 8.8.4.4

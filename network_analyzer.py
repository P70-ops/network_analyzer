#!/usr/bin/env python3
"""
Network Information Tool
-----------------------
A comprehensive tool to display:
- Routing tables
- Network interfaces
- ARP cache
- DNS information
- Default gateways
"""

import os
import re
import subprocess
import platform
import netifaces
from prettytable import PrettyTable

class NetworkAnalyzer:
    def __init__(self):
        self.system = platform.system()
        self.interface_details = {}
        self.routing_table = []
        self.arp_table = ""
        self.dns_info = ""
        self.gateway_info = {}

    def collect_all_info(self):
        """Collect all network information"""
        self.routing_table = self.get_routing_table()
        self.interface_details = self.get_interface_details()
        self.arp_table = self.get_arp_table()
        self.dns_info = self.get_dns_info()
        self.gateway_info = netifaces.gateways().get('default', {})

    def get_routing_table(self):
        """Get system routing table"""
        if self.system == "Windows":
            return self.get_windows_routing_table()
        elif self.system in ["Linux", "Darwin"]:
            return self.get_unix_routing_table()
        else:
            return {"error": "Unsupported operating system"}

    def get_windows_routing_table(self):
        """Get Windows routing table"""
        try:
            result = subprocess.check_output("route print", shell=True).decode('utf-8', 'ignore')
            return self.parse_windows_route(result)
        except Exception as e:
            return {"error": str(e)}

    def get_unix_routing_table(self):
        """Get Unix/Linux routing table"""
        try:
            result = subprocess.check_output("netstat -rn", shell=True).decode('utf-8', 'ignore')
            return self.parse_unix_route(result)
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def parse_windows_route(output):
        """Parse Windows route output"""
        routes = []
        for line in output.split('\n'):
            line = line.strip()
            if line.startswith("0.0.0.0"):
                parts = re.split(r'\s+', line)
                if len(parts) >= 5:
                    routes.append({
                        "Destination": parts[0],
                        "Netmask": parts[1],
                        "Gateway": parts[2],
                        "Interface": parts[3],
                        "Metric": parts[4] if len(parts) > 4 else ""
                    })
        return routes

    @staticmethod
    def parse_unix_route(output):
        """Parse Unix route output"""
        routes = []
        for line in output.split('\n'):
            line = line.strip()
            if line.startswith("default") or line.startswith("0.0.0.0"):
                parts = re.split(r'\s+', line)
                if len(parts) >= 4:
                    routes.append({
                        "Destination": "default" if parts[0] == "default" else parts[0],
                        "Gateway": parts[1],
                        "Genmask": parts[2] if len(parts) > 2 else "",
                        "Flags": parts[3] if len(parts) > 3 else "",
                        "Interface": parts[5] if len(parts) > 5 else ""
                    })
            elif re.match(r'^\d+\.\d+\.\d+\.\d+', line):
                parts = re.split(r'\s+', line)
                if len(parts) >= 5:
                    routes.append({
                        "Destination": parts[0],
                        "Gateway": parts[1],
                        "Genmask": parts[2],
                        "Flags": parts[3],
                        "Interface": parts[5] if len(parts) > 5 else ""
                    })
        return routes

    @staticmethod
    def get_interface_details():
        """Get detailed interface information"""
        interfaces = {}
        for interface in netifaces.interfaces():
            try:
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    interfaces[interface] = {
                        'IP': addrs[netifaces.AF_INET][0]['addr'],
                        'Netmask': addrs[netifaces.AF_INET][0]['netmask'],
                        'MAC': addrs[netifaces.AF_LINK][0]['addr'] if netifaces.AF_LINK in addrs else None,
                        'Broadcast': addrs[netifaces.AF_INET][0].get('broadcast', 'N/A')
                    }
            except (ValueError, KeyError):
                continue
        return interfaces

    def get_arp_table(self):
        """Get system ARP table"""
        try:
            if self.system == "Windows":
                return subprocess.check_output("arp -a", shell=True).decode('utf-8', 'ignore')
            else:
                return subprocess.check_output("arp -n", shell=True).decode('utf-8', 'ignore')
        except Exception as e:
            return f"Error getting ARP table: {str(e)}"

    def get_dns_info(self):
        """Get DNS server information"""
        try:
            if self.system == "Windows":
                return subprocess.check_output("ipconfig /all", shell=True).decode('utf-8', 'ignore')
            else:
                return subprocess.check_output("cat /etc/resolv.conf", shell=True).decode('utf-8', 'ignore')
        except Exception as e:
            return f"Error getting DNS info: {str(e)}"

    def display_all_info(self):
        """Display all collected network information"""
        print("\n" + "="*80)
        print("NETWORK INFORMATION TOOL".center(80))
        print("="*80)

        self.display_routing_table()
        self.display_interfaces()
        self.display_gateways()
        self.display_arp_table()
        self.display_dns_info()

    def display_routing_table(self):
        """Display routing table"""
        print("\n" + "-"*80)
        print("ROUTING TABLE".center(80))
        print("-"*80)
        
        if isinstance(self.routing_table, dict) and 'error' in self.routing_table:
            print(f"\nError: {self.routing_table['error']}")
            return

        table = PrettyTable()
        table.field_names = ["Destination", "Gateway", "Netmask", "Interface", "Metric/Flags"]
        table.align = "l"
        
        for route in self.routing_table:
            table.add_row([
                route.get("Destination", "N/A"),
                route.get("Gateway", "N/A"),
                route.get("Netmask", route.get("Genmask", "N/A")),
                route.get("Interface", "N/A"),
                route.get("Metric", route.get("Flags", "N/A"))
            ])
        
        print(table)

    def display_interfaces(self):
        """Display network interfaces"""
        print("\n" + "-"*80)
        print("NETWORK INTERFACES".center(80))
        print("-"*80)
        
        if not self.interface_details:
            print("No interface information available")
            return

        table = PrettyTable()
        table.field_names = ["Interface", "IP Address", "Netmask", "MAC Address", "Broadcast"]
        table.align = "l"
        
        for iface, details in self.interface_details.items():
            table.add_row([
                iface,
                details['IP'],
                details['Netmask'],
                details['MAC'] or "N/A",
                details.get('Broadcast', 'N/A')
            ])
        
        print(table)

    def display_gateways(self):
        """Display gateway information"""
        print("\n" + "-"*80)
        print("DEFAULT GATEWAYS".center(80))
        print("-"*80)
        
        if not self.gateway_info:
            print("No gateway information available")
            return

        table = PrettyTable()
        table.field_names = ["Type", "Gateway IP", "Interface"]
        table.align = "l"
        
        for family, gateway_info in self.gateway_info.items():
            if len(gateway_info) >= 2:
                table.add_row([
                    "IPv4" if family == netifaces.AF_INET else "IPv6",
                    gateway_info[0],
                    gateway_info[1]
                ])
        
        print(table)

    def display_arp_table(self):
        """Display ARP table"""
        print("\n" + "-"*80)
        print("ARP TABLE".center(80))
        print("-"*80)
        print(self.arp_table)

    def display_dns_info(self):
        """Display DNS information"""
        print("\n" + "-"*80)
        print("DNS INFORMATION".center(80))
        print("-"*80)
        print(self.dns_info)

def check_dependencies():
    """Check for required dependencies"""
    missing = []
    try:
        import netifaces
    except ImportError:
        missing.append("netifaces (pip install netifaces)")
    
    try:
        from prettytable import PrettyTable
    except ImportError:
        missing.append("prettytable (pip install prettytable)")
    
    if missing:
        print("Missing dependencies:")
        for dep in missing:
            print(f"- {dep}")
        return False
    return True

if __name__ == "__main__":
    if not check_dependencies():
        exit(1)
    
    analyzer = NetworkAnalyzer()
    analyzer.collect_all_info()
    analyzer.display_all_info()

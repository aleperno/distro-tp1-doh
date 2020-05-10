import dns.resolver


def resolve_host(host):
    """
    Resolves a host and returns the list of associated ips
    """
    addresses = []
    ttl = 0
    try:
        result = dns.resolver.query(host, "A")
        ttl = result.rrset.ttl
        for item in result:
            addresses.append(item.address)
    except dns.resolver.NXDOMAIN as e:
        pass

    return ttl, addresses

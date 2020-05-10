from itertools import cycle
from datetime import datetime, timedelta


class Domain(object):
    def __init__(self, domain, addrs=None, ttl=0, custom=False):
        self.domain = domain
        self.ttl = ttl
        self.addrs = addrs if addrs else []
        self.cycle = cycle(self.addrs)
        self.expires = (ttl != 0)
        self.expiration = datetime.utcnow() + timedelta(seconds=ttl)
        self.custom = custom

    @property
    def expired(self):
        if self.expires:
            return datetime.utcnow() >= self.expiration
        return False

    @property
    def ip(self):
        return next(self.cycle)

    def as_dict(self):
        d = {
            "domain": self.domain,
            "ip": self.ip,
            "custom": self.custom
        }
        return d

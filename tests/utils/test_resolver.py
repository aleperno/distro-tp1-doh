from utils.resolver import resolve_host
from dns.resolver import NXDOMAIN


class MockedQuery(object):
    def __init__(self, addresses=None, ttl=0):
        self.addr = addresses if addresses else []
        self.iter_n = -1
        self._ttl = ttl

    def __iter__(self):
        return self

    def __next__(self):
        if self.iter_n+1 < len(self.addr):
            self.iter_n += 1
            return self
        raise StopIteration()

    @property
    def rrset(self):
        return self

    @property
    def ttl(self):
        return self._ttl

    @property
    def address(self):
        return self.addr[self.iter_n]


def test_call(mocker):
    query_f = mocker.patch('utils.resolver.dns.resolver.query')

    resolve_host('foo')

    query_f.assert_called_once_with('foo', 'A')


def test_multiple_a_records(mocker):
    addrs = ['foo', 'bar', 'dummy']
    mocked_response = MockedQuery(addresses=addrs, ttl=1800)

    mocker.patch('utils.resolver.dns.resolver.query', return_value=mocked_response)

    assert resolve_host('google.com') == (1800, addrs)


def test_unknown_host(mocker):
    mocker.patch('utils.resolver.dns.resolver.query', side_effect=NXDOMAIN)

    assert resolve_host('google.com') == (0, [])
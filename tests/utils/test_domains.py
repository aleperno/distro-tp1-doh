import pytest
from utils.domains import Domain
from freezegun import freeze_time
from datetime import datetime


def test_cyclying_domains():
    domains = Domain('foo.com', addrs=[1, 2, 3])

    assert domains.ip == 1
    assert domains.ip == 2
    assert domains.ip == 3
    assert domains.ip == 1

    assert domains.expires == False


def test_expiration():
    with freeze_time('2020-05-10 17:30:00') as frozen_time:
        domain = Domain('foo.com', ttl=60*30)

        assert domain.expires
        assert not domain.expired

        frozen_time.move_to('2020-05-10 18:00:00')

        assert domain.expired


@pytest.mark.parametrize('custom', (True, False))
def test_domain_data(custom):
    domain = Domain('testing.com', addrs=['10.20.0.4'], custom=custom)

    assert domain.as_dict() == {'domain': 'testing.com',
                                'ip': '10.20.0.4',
                                'custom': custom}


from flask import make_response
from utils.resolver import resolve_host
from utils.domains import Domain
import re

domains = {}

custom_domains = {}

def check_custom_domain_kw(required, **kwargs):
    """
    Checks Domain and IP are present in the kwargs
    """
    print(f"Los kw son {kwargs}")
    for req in required:
        if req not in kwargs:
            return False
    return True


def resolve_and_store(domain):
    ttl, addrs = resolve_host(domain)
    if addrs:
        new = Domain(domain=domain, addrs=addrs, ttl=ttl, custom=False)
        domains[domain] = new
        return new
    else:
        return None


def obtener_dominio(domain):
    """
    Maneja el `/api/domains/<domain>`
    """

    if domain in custom_domains:
        print("Existe el dominio custom")
        return make_response(custom_domains[domain].as_dict(), 200)
    elif domain in domains:
        print("Existe el dominio")
        obj = domains[domain]
        if not obj.expired:
            return make_response(obj.as_dict(), 200)

    # Ese bloque se ejecuta si no se encontró el dominio, o se encontró y se encuentra expirado
    # Intento resolverlo
    print(f"Intento resolver dominio {domain}")
    new = resolve_and_store(domain)
    if not new:
        # No se pudo resolver
        return make_response({'error': "domain not found"}, 404)

    return make_response(new.as_dict(), 200)


def create_custom_domain(**kwargs):
    body = kwargs.get('body')
    if not check_custom_domain_kw(required=('domain', 'ip'), **body):
        return make_response({'error': 'Missing data'}, 400)
    domain = body.get('domain')
    ip = body.get('ip')
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",ip):
        return make_response({'error': "Invalid Format for IP Address (field 'ip')"}, 400)
    if domain in custom_domains:
        return make_response({'error': 'custom domain already exists'}, 400)

    obj = Domain(domain=domain, addrs=[ip], custom=True, ttl=0)
    custom_domains[domain] = obj

    return make_response(obj.as_dict(), 201)


def modify_custom_domain(**kwargs):
    body = kwargs.get('body')
    domain = kwargs.get('domain')
    if not check_custom_domain_kw(required=('ip',), **body) or \
       not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", body.get('ip')):
        return make_response({'error': 'payload is invalid'}, 400)

    ip = body.get('ip')

    if domain not in custom_domains:
        return make_response({'error': 'domain not found'}, 404)

    obj = Domain(domain=domain, addrs=[ip], custom=True, ttl=0)
    custom_domains[domain] = obj

    return make_response(obj.as_dict(), 200)


def delete_custom_domain(domain):
    if domain not in custom_domains:
        return make_response({'error': 'domain not found'}, 404)

    custom_domains.pop(domain)
    return make_response({'domain': domain}, 200)


def query_domains(q):
    items = []
    for domain, obj in custom_domains.items():
        if q in domain:
            items.append(obj)

    response = {'items': [d.as_dict() for d in items]}
    return make_response(response, 200)

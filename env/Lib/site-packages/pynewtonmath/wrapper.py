from . import core


# Expose basic endpoints
core.expose_endpoints(core.sys.modules[__name__], *core.ENDPOINTS)


# Extend complex endpoint functionality
def log (exp, base=None):
    return core.log('%d|%s' % (base, exp) if base else exp)


def tangent (exp, x=None):
    return core.tangent('%d|%s' % (x, exp) if x else exp)


def area (exp, start=None, end=None):
    return core.area('%d:%d|%s' % (start, end, exp) if start and end else exp)

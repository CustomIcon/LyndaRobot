import json
import sys
import urllib.parse
import urllib.request


ENDPOINTS = ['simplify', 'factor', 'derive', 'integrate', 'zeroes', 'tangent',
             'area', 'cos', 'sin', 'tan', 'arccos', 'arcsin', 'arctan', 'abs',
             'log']


def send_request (operation, expression):
    """
    Send an HTTP GET request to the newton API
    operation: one of the API endpoints
    expression: the str for the given endpoint to evaluate
    """
    
    base = 'https://newton.now.sh'
    url = '%s/%s/%s' % (base, operation, urllib.parse.quote(expression))
    
    with urllib.request.urlopen(url) as response:
        return handle_response(response)


def handle_response (response):
    """
    Handle a response from the newton API
    """
    
    response = json.loads(response.read())
    
    # Was the expression valid?
    if 'error' in response:
        raise ValueError(response['error'])
    else:
        # Some of the strings returned can be parsed to integers or floats
        try:
            return json.loads(response['result'])
        except (TypeError, json.decoder.JSONDecodeError):
            # If the result is NaN, return the actual NaN float
            if response['result'] == 'NaN':
                return float('nan')
            else:
                return response['result']


def expose_endpoints (module, *args):
    """
    Expose methods to the given module for each API endpoint
    """
    
    for op in args:
        # Capture the closure state
        def create_method (o):
            return lambda exp: send_request(o, exp)
        
        setattr(sys.modules[__name__], op, create_method(op))
        setattr(module, op, getattr(sys.modules[__name__], op))

import json
from flask import request, abort
import requests
from functools import wraps
from jose import jwt, jwk
from urllib.request import urlopen

JWKS_URL = 'https://dev-80n7ot50j6bt430j.us.auth0.com/.well-known/jwks.json'
AUTH0_DOMAIN = 'dev-80n7ot50j6bt430j.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'render'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# referenced from https://learn.udacity.com/nanodegrees/nd0044/parts/cd0039/lessons/3bd56b2d-7a3f-4aff-90f8-842eec9071a9/concepts/4aa951ce-d926-4162-8393-c8ed33b1bdfa?_gl=1*5znt0s*_gcl_au*MTUyMTEzNTc5NS4xNzE4MzQ4MDky*_ga*MTQzOTU0MTY2OS4xNzE4MzQ4MTUy*_ga_CF22GKVCFK*MTcyMzA5MjQ0MC4xLjEuMTcyMzA5MjQ0OC41Mi4wLjA.&lesson_tab=lesson


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        abort(401)
    
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')
    
    if len(header_parts) != 2:
        abort(401)
    elif header_parts[0].lower() != 'bearer':
        abort(401)
    
    print(f"Header parts: {header_parts}")
    return header_parts[1]

# referenced from https://learn.udacity.com/nanodegrees/nd0044/parts/cd0039/lessons/586b8e66-f53c-4225-bba0-a899e8eba154/concepts/33a0cccd-a3e0-4767-9bd8-7533d217d3ec?_gl=1*5znt0s*_gcl_au*MTUyMTEzNTc5NS4xNzE4MzQ4MDky*_ga*MTQzOTU0MTY2OS4xNzE4MzQ4MTUy*_ga_CF22GKVCFK*MTcyMzA5MjQ0MC4xLjEuMTcyMzA5MjQ0OC41Mi4wLjA.&lesson_tab=lesson


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True

# referenced from https://learn.udacity.com/nanodegrees/nd0044/parts/cd0039/lessons/586b8e66-f53c-4225-bba0-a899e8eba154/concepts/d46f3740-d5d8-41bb-a92a-fe00b1e7438e?_gl=1*5znt0s*_gcl_au*MTUyMTEzNTc5NS4xNzE4MzQ4MDky*_ga*MTQzOTU0MTY2OS4xNzE4MzQ4MTUy*_ga_CF22GKVCFK*MTcyMzA5MjQ0MC4xLjEuMTcyMzA5MjQ0OC41Mi4wLjA.&lesson_tab=lesson


def get_jwks():
    try:
        response = requests.get(JWKS_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to find appropriate key.'
        }, 500)
    except Exception as err:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to connect to Auth0.'
        }, 500)

def get_public_key(kid, jwks):
    for key in jwks.get('keys', []):
        if key.get('kid') == kid:
            # Construct the public key from the JWK
            return jwk.construct(key).to_pem()
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find appropriate key.'
    }, 401)

def verify_decode_jwt(token):
    try:
        # Decode the token header to get the key id (kid)
        header = jwt.get_unverified_header(token)
        kid = header.get('kid')
        if not kid:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }, 401)

        # Fetch the JWKS and get the public key for the kid
        jwks = get_jwks()
        public_key = get_public_key(kid, jwks)

        # Verify and decode the JWT
        payload = jwt.decode(
            token,
            public_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f'https://{AUTH0_DOMAIN}/'
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'token_expired',
            'description': 'Token expired.'
        }, 401)
    except jwt.JWTClaimsError:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Invalid claims in token.'
        }, 401)
    except jwt.JWSError:
        raise AuthError({
            'code': 'invalid_token',
            'description': 'Invalid token.'
        }, 401)
    except Exception as e:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to parse authentication token.'
        }, 401)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator

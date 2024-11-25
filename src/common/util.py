import os
import requests


# Function to set default headers, including dynamic Authorization token
def get_headers(custom_headers=None):
    headers = custom_headers or {}
    auth_token = os.getenv('AUTH_TOKEN')
    if auth_token:
        headers['Authorization'] = f'{auth_token}'
    return headers


def get(url, headers=None, params=None, body=None):
    try:
        # Manually handle the body for GET, as `requests.get` doesn’t support it directly.
        if body:
            response = requests.request('GET', url, headers=get_headers(headers), params=params, json=body)
        else:
            response = requests.get(url, headers=get_headers(headers), params=params)

        # Raise an exception for non-2xx responses
        response.raise_for_status()

        return {'status': response.status_code, 'body': response.json(), 'error': None}
    except requests.exceptions.RequestException as e:
        return {'status': None, 'body': None, 'error': str(e)}


def post(url, body=None, headers=None, params=None):
    try:
        response = requests.post(url, json=body, headers=get_headers(headers), params=params)
        response.raise_for_status()
        return {'status': response.status_code, 'body': response.json(), 'error': None}
    except requests.exceptions.RequestException as e:
        return {'status': None, 'body': None, 'error': str(e)}


def put(url, body=None, headers=None, params=None):
    try:
        response = requests.put(url, json=body, headers=get_headers(headers), params=params)
        response.raise_for_status()
        return {'status': response.status_code, 'body': response.json(), 'error': None}
    except requests.exceptions.RequestException as e:
        return {'status': None, 'body': None, 'error': str(e)}


def delete(url, headers=None, params=None, body=None):
    try:
        # Use `requests.request` to allow the body in DELETE requests.
        if body:
            response = requests.request('DELETE', url, headers=get_headers(headers), params=params, json=body)
        else:
            response = requests.delete(url, headers=get_headers(headers), params=params)

        response.raise_for_status()
        return {'status': response.status_code, 'body': response.json(), 'error': None}
    except requests.exceptions.RequestException as e:
        return {'status': None, 'body': None, 'error': str(e)}

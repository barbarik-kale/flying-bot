import os

base_url = os.getenv('BASE_URL', 'http://localhost:8000')
urls = {
    'user': f'{base_url}/user/',
    'drone': f'{base_url}/drone/'
}


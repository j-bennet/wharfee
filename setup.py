
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Docker-CLI',
    'author': 'Iryna Truong',
    'url': 'http://www.docker-cli.com.',
    'download_url': 'http://www.docker-cli/latest.',
    'author_email': 'i.chernyavska@gmail.com.',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['dockercli'],
    'scripts': [],
    'name': 'dockercli'
}

setup(**config)

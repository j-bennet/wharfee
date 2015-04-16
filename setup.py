
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Docker-CLI',
    'author': 'Iryna Truong',
    'url': 'http://www.docker-cli.com.',
    'download_url': 'http://www.docker-cli/latest.',
    'author_email': 'i[dot]chernyavska[at]gmail[dot]com.',
    'version': '0.1',
    'install_requires': [
        'prompt_toolkit',
        'docker-py',
        'tabulate',
        'click'
    ],
    'entry_points': {
        'console_scripts': 'dockercli = dockercli.main:cli'
    },
    'packages': ['dockercli'],
    'scripts': [],
    'name': 'dockercli'
}

setup(**config)


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    description='Docker-CLI',
    author='Iryna Truong',
    url='http://www.docker-cli.com.',
    download_url='http://www.docker-cli/latest.',
    author_email='i[dot]chernyavska[at]gmail[dot]com.',
    version='0.1',
    install_requires=[
        'pygments>=2.0.2',
        'prompt-toolkit==0.32',
        'docker-py>=1.1.0',
        'tabulate>=0.7.5',
        'click>=4.0'
    ],
    extras_require={
        'testing': ['pytest', 'mock'],
    },
    entry_points={
        'console_scripts': 'dockercli = dockercli.main:cli'
    },
    packages=['dockercli'],
    scripts=[],
    name='dockercli'
)
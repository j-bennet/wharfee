from wharfee.__init__ import __version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    description='Wharfee: a shell for Docker',
    author='Iryna Cherniavska',
    url='http://wharfee.com',
    download_url='http://github.com/j-bennet/wharfee',
    author_email='i[dot]chernyavska[at]gmail[dot]com',
    version=__version__,
    license='LICENSE.txt',
    install_requires=[
        'six>=1.9.0',
        'pygments>=2.0.2',
        'prompt_toolkit>=1.0.0,<1.1.0',
        'docker-py>=1.6.0',
        'tabulate>=0.7.5',
        'click>=4.0',
        'py-pretty>-0.1',
        'configobj>=5.0.6',
        'pexpect>=3.3',
        'fuzzyfinder>=1.0.0'
    ],
    extras_require={
        'testing': [
            'pytest>=2.7.0',
            'mock>=1.0.1',
            'tox>=1.9.2'
        ],
    },
    entry_points={
        'console_scripts': 'wharfee = wharfee.main:cli'
    },
    packages=['wharfee'],
    package_data={'wharfee': ['wharfeerc']},
    scripts=[],
    name='wharfee',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

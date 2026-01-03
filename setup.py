from wharfee.__init__ import __version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    description='Wharfee: a shell for Docker',
    author='Irina Truong',
    url='http://wharfee.com',
    download_url='http://github.com/j-bennet/wharfee',
    author_email='i[dot]chernyavska[at]gmail[dot]com',
    version=__version__,
    license='LICENSE.txt',
    install_requires=[
        'pygments>=2.0.2',
        'prompt_toolkit>=3.0.0',
        'docker>=7.0.0',
        'tabulate>=0.7.5',
        'click>=4.0',
        'py-pretty>=0.1',
        'configobj>=5.0.6',
        'pexpect>=3.3',
        'fuzzyfinder>=1.0.0',
        'ruamel.yaml>=0.15.72',
    ],
    extras_require={
        'testing': [
            'pytest>=2.7.0',
            'mock>=1.0.1',
            'tox>=1.9.2'
        ],
    },
    entry_points={
        'console_scripts': [
            'wharfee = wharfee.main:cli',
            'wharfee-ops = scripts.optionizer:main',
        ]
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

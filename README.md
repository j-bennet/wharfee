[![Stories in Ready](https://badge.waffle.io/j-bennet/wharfee.png?label=ready&title=Ready)](https://waffle.io/j-bennet/wharfee)
[![PyPI version](https://badge.fury.io/py/wharfee.svg)](http://badge.fury.io/py/wharfee)
[![Join the chat at https://gitter.im/j-bennet/wharfee](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/j-bennet/wharfee?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
# wharfee

A shell for Docker that can do autocompletion and syntax highlighting.

## Why?

Docker commands have tons of options. They are hard to remember.

![ps](screenshots/ps-containers.png)

Container names are hard to remember and type.

![rm](screenshots/rm-containers.png)

Same goes for image names.

![rmi](screenshots/rmi-images.png)

There are some handy shortcuts too. What was that command to remove all dangling images? OMG, what was it? docker rmi $(docker ps --all --quiet)? Oh, there you go:

![rmi-dangling](screenshots/rmi-all-dangling.png)

Boom! How about removing all stopped containers?

![rm-stopped](screenshots/rm-all-stopped.png)

## Installation

Wharfee is a Python package hosted on pypi and installed with:

    $ pip install wharfee
    
Alternatively, you can install the latest from github and get all the bugfixes that didn't make it into pypi release yet:

    $ pip install git+https://github.com/j-bennet/wharfee.git

## What are you using?

* To talk to Docker: [docker-py](https://github.com/docker/docker-py).
* To power the CLI: [Python Prompt Toolkit](http://github.com/jonathanslenders/python-prompt-toolkit).
* To format the output: [tabulate](https://pypi.python.org/pypi/tabulate).
* To print out the output: [Click](http://click.pocoo.org/3/).

## Can I contribute?

Yes! Pull request or [issues](https://github.com/j-bennet/wharfee/issues) are welcome.

## How do you test it?

First, install the requirements for testing:

    $ pip install -r requirements-dev.txt

There are unit tests under *tests*. The command to run them is:

    $ py.test

Additionally, there are integration tests, that can be run with:

    $ cd tests
    $ behave

To see stdout/stderr, use the following command:

    $ behave --no-capture

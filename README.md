[![Stories in Ready](https://badge.waffle.io/j-bennet/dockercli.png?label=ready&title=Ready)](https://waffle.io/j-bennet/dockercli)
# dockercli
A CLI with autocompletion and syntax highlighting for Docker commands.

## Why?

Docker commands have tons of options. They are hard to remember.

![ps](screenshots/ps-containers.png)

Container names are hard to remember and type.

![rm](screenshots/rm-containers.png)

Same goes for image names.

![rmi](screenshots/rmi-images.png)

## What are you using?

* To talk to Docker: [docker-py](https://github.com/docker/docker-py).
* To power the CLI: [Python Prompt Toolkit](http://github.com/jonathanslenders/python-prompt-toolkit).
* To format the output: [tabulate](https://pypi.python.org/pypi/tabulate).
* To print out the output: [Click](http://click.pocoo.org/3/).

## Is it perfect?

Not... yet.

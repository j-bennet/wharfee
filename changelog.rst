0.2
====

Features:
---------

* Configuration file .dockerclirc, where timeout and visual style can be
  specified.

Bug fixes:
----------

* Catch-all clause for exceptions to avoid an ugly stack trace.
* Timeout for attaching to a Docker service.

0.1
====

Features:
---------

* Syntax highlighting for implemented commands and options.
* Autocomplete for commands, container names, image names.
* Help for available commands.
* Supported commands (with basic options)::

  version
  ps
  pull
  images
  info
  inspect
  run
  rm
  rmi
  search
  start
  stop
  top

Not supported:
--------------

* "run" in tty/interactive mode.
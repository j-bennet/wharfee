0.6.1
=====

Bug fixes:
----------

* Fix for the crash on image names with ':' (thanks `Sean https://github.com/seanch87`_).

0.5-0.6
=======

Version bumped up because of erroneous releases to PyPi.

0.4
===

Bug fixes:
----------

* Fix for missing file on startup (thanks `Amjith https://github.com/amjith`_).

0.3
===

Features:
---------

* More supported commands:

::

  attach
  build
  clear
  create
  exec
  login
  logs
  pause
  port
  push
  restart
  shell (shortcat for "exec <container name> <shell command>")
  tag
  top
  unpause

* Implemented interactive terminal mode for "start", "run" and "exec".
* Added fuzzy matching option to completion suggestions.
* Completer can suggest either short or long option names.
* Added more options to "run", including volumes, ports and and links.
* Non-standard options are moved into a separate group in command help.
* Prettier formatting of "images" and "ps" output.

Bug fixes:
----------

* Completer crashing on unexpected characters.
* Completer crashing inside an unfinished quoted string.

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
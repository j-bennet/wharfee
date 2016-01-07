0.7
===

Features:
---------

* Added "volume" commands:

::

  volume create
  volume rm
  volume ls
  volume inspect

* Added ``--all`` shortcut option to ``rm`` and ``rmi`` commands.
* Internal fixes and updates (thanks: `Anthony DiSanti`_, `Arthur Skowronek`_).

0.6.8
=====

* Fix for "port" command not returning anything (#100).
* Fix for "--publish" not publishing the ports (#90).

0.6.7
=====

Fixes and travis updates.

0.6.6
=====

* Fixes to support python 2.6.
* Added logging (finally).

0.6.5
=====

Features:
---------

* Updated `Python Prompt Toolkit`_ to 0.46. This adds the following features:

  * Ctrl + Z puts the application into background (suspends it). Use "fg" command to bring it back.
  * Meta + ! brings up "system prompt".

* Support for using TLS and DOCKER_* variables with Swarm (thanks `achied`_).
* Colorized output of "inspect".

Bug fixes:
----------

* Fixed completer crashing when trying to autocomplete Unicode characters.
* Fixed external CLI call when environment variable contains spaces.

0.6.1-0.6.4
===========

Features:
---------

* Added "refresh" command to force refresh of autocompletions.

Bug fixes:
----------

* Fix for the crash on image names with ':' (thanks `Sean`_).
* Fix for incorrect handling of "attach" in external CLI call.
* Fix for an error when running with --publish port:port and --detach (#80).
* Fix for "exec" failing because of "interactive" parameter passed in erroneously (#92).

0.5-0.6
=======

Version bumped up because of erroneous releases to PyPi.

0.4
===

Bug fixes:
----------

* Fix for missing file on startup (thanks `Amjith`_).

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

.. _`Amjith`: https://github.com/amjith
.. _`Anthony DiSanti`: https://github.com/AnthonyDiSanti
.. _`Arthur Skowronek`: https://github.com/eisensheng
.. _`Sean`: https://github.com/seanch87
.. _`achied`: https://github.com/achied
.. _`Python Prompt Toolkit`: http://github.com/jonathanslenders/python-prompt-toolkit

Feature: call container-related commands

  Scenario: run container
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we run container hello with image hello-world
      then we see "Hello from Docker!" printed out

  Scenario: create and start container
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we create container hello with image hello-world
      then we see id string
      when we start container hello
      then we see hello at line end

  Scenario: remove container
     Given we have wharfee installed
      when we run wharfee
      then we see wharfee prompt
      when we run container hello with image hello-world
      then we see "Hello from Docker!" printed out
      when we remove container hello
      then we see hello at line end

  Scenario: check ports
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we run container foo with image busybox and command /bin/sh and options -d -i -t
      and we wait for prompt
      then we see "Interactive terminal is closed" printed out
      when we check ports for container foo
      then we see "There are no port mappings" printed out

  Scenario: pause and unpause
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we run container foo with image busybox and command /bin/sh and options -d -i -t
      and we wait for prompt
      then we see "Interactive terminal is closed" printed out
      when we pause container foo
      then we see container foo paused
      when we unpause container foo
      then we see container foo unpaused

  Scenario: run, exec, stop
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we run container foo with image busybox and command /bin/sh and options -d -i -t
      and we wait for prompt
      then we see "Interactive terminal is closed" printed out
      when we execute ls -l / in container foo
      then we see total 36 at line end
      when we stop container foo
      then we see foo at line end

  Scenario: run, exec, kill
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we run container foo with image busybox and command /bin/sh and options -d -i -t
      and we wait for prompt
      then we see "Interactive terminal is closed" printed out
      when we execute ls -l / in container foo
      then we see total 36 at line end
      when we kill container foo
      then we see foo at line end

  Scenario: shell to container
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we run container foo with image busybox and command /bin/sh and options -d -i -t
      and we wait for prompt
      then we see "Interactive terminal is closed" printed out
      when we open shell to container foo and /bin/sh
      then we see # printed out
      when we send "ctrl + d"
      then we see "Shell to foo is closed" printed out

  Scenario: see top processes
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we run container foo with image busybox and command /bin/sh and options -d -i -t
      and we wait for prompt
      then we see "Interactive terminal is closed" printed out
      when we view top for container foo
      then we see top processes

  Scenario: restart container
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we run container foo with image busybox and command /bin/sh and options -d -i -t
      and we wait for prompt
      then we see "Interactive terminal is closed" printed out
      when we restart container foo
      then we see foo restarted

  Scenario: list containers with nothing running
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we list containers
      then we see "There are no containers to list" printed out

  Scenario: list containers, force remove container
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we run container foo with image busybox and command /bin/sh and options -d -i -t
      and we wait for prompt
      then we see "Interactive terminal is closed" printed out
      when we list containers
      then we see Status printed out
      when we force remove container foo
      then we see foo at line end

  Scenario: see container logs
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we run container hello with image hello-world
      then we see "Hello from Docker!" printed out
      when we wait for prompt
      and we see logs for container hello
      then we see "Hello from Docker!" printed out

  Scenario: attach and detach
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we run container foo with image busybox and command /bin/sh and options -d -i -t
      and we wait for prompt
      then we see "Interactive terminal is closed" printed out
      when we attach to container foo
      then we see # printed out
      when we detach from container foo
      then we see "Detached from foo" printed out

  Scenario: remove stopped containers
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we run container hello with image hello-world
      then we see "Hello from Docker!" printed out
      when we wait for prompt
      and we remove stopped containers
      then we see id string

  Scenario: rename container
     Given we have wharfee installed
     when we run wharfee
     and we wait for prompt
     when we run container foo with image busybox and command /bin/sh and options -d -i -t
     and we wait for prompt
     then we see "Interactive terminal is closed" printed out
     when we rename container foo to bar
     and we wait for prompt
     then we see container bar running

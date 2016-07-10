Feature: call container-related commands

  Scenario: run container
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we run container hello with image hello-world
      then we see "Hello from Docker!" printed out

  Scenario: remove container
     Given we have wharfee installed
      when we run wharfee
      then we see wharfee prompt
      when we remove container hello
      then we see hello at line end

  Scenario: run container, exec, stop, rm
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
      when we remove container foo
      then we see foo at line end

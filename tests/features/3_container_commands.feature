Feature: call container-related commands

  Scenario: run container
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we run container hello with image hello-world
      then we see "Hello from Docker!" printed out

  @wip
  Scenario: remove container
     Given we have wharfee installed
      when we run wharfee
      then we see wharfee prompt
      when we remove container hello
      then we see hello at line end

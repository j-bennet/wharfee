Feature: run the cli,
  call the help command,
  exit the cli

  Scenario: run the cli
     Given we have dockercli installed
      when we run dockercli
      then we see dockercli prompt

  Scenario: run "help" command
     Given we have dockercli installed
      when we run dockercli
      and we wait for prompt
      and we send "help" command
      then we see help output

  Scenario: run the cli and exit
     Given we have dockercli installed
      when we run dockercli
      and we wait for prompt
      and we send "ctrl + d"
      then dockercli exits

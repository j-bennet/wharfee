Feature: run the cli,
  call the help command,
  exit the cli

  Scenario: run the cli
     Given we have wharfee installed
      when we run wharfee
      then we see wharfee prompt

  Scenario: run "help" command
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      and we send "help" command
      then we see help output

  Scenario: run "clear" command
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      and we clear screen
      then we see wharfee prompt

  Scenario: run "refresh" command
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      and we refresh completions
      then we see "Refreshed completions" printed out

  Scenario: run the cli and exit
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      and we send "ctrl + d"
      then wharfee exits

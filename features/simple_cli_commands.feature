Feature: run the cli,
  call the help command,
  exit the cli

  Scenario: run the cli
     Given we have dockercli installed
      when we run dockercli
      then we see dockercli prompt

#  Scenario: run "help" command
#     Given we have dockercli installed
#      when we run dockercli
#      and we send "help" command
#      then we see help output

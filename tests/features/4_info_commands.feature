Feature: call info commands

  Scenario: check info
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we ask for docker info
      then we see "SystemTime:" printed out

  Scenario: check version
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we ask for docker version
      then we see "ApiVersion" printed out

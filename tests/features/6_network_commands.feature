Feature: call network commands

  Scenario: create network and remove network
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we create network simple-network
      then we see id string
      when we remove network simple-network
      then we see simple-network at line end

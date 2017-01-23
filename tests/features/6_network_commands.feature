Feature: call network commands

  Scenario: create network
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we create network foonetwork
      then we see id string

  Scenario: list networks
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we list networks
      then we see -- at line end
      and we see id string

  Scenario: inspect network
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we inspect network foonetwork
      then we see foonetwork printed out

  Scenario: remove network
    Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we remove network foonetwork
      then we see foonetwork at line end

  Scenario: prune networks
    Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we create network boonetwork
      then we see id string
      when we prune networks
      then we see boonetwork at line end

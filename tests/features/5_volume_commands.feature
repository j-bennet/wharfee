Feature: call volume commands

  Scenario: list volumes
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we list volumes
      then we see "There are no volumes to list" printed out

  Scenario: create, inspect, remove volume
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we create volume foo
      then we see foo at line end
      when we list volumes
      then we see local printed out
      when we inspect volume foo
      then we see Driver printed out
      when we remove volume foo
      then we see foo at line end

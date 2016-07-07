Feature: call image-related commands

  Scenario: build image from Dockerfile
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      and we build image from Dockerfile
      then we see image built

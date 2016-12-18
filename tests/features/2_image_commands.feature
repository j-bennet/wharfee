Feature: call image-related commands

  Scenario: build image from Dockerfile
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      and we build test-image from Dockerfile
      then we see image built

  Scenario: pull hello-world image
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      and we pull hello-world:latest image
      then we see hello-world pulled
      and we see wharfee prompt

  Scenario: list images
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we list images
      then we see image hello-world listed

  Scenario: inspect image
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we inspect image hello-world
      then we see "/hello" printed out

  Scenario: log in as user wharfee
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      and we log in as wharfee, wharfee.cli@gmail.com with docker.me
      then we see login success

  Scenario: tag an image
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we tag test-image into wharfee/test-image:version1.0
      then we see test-image tagged into wharfee/test-image:version1.0

  Scenario: remove an image
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we remove image wharfee/test-image:version1.0
      then we see image wharfee/test-image:version1.0 removed
      when we remove image test-image
      then we see image test-image removed

  Scenario: search images
     Given we have wharfee installed
      when we run wharfee
      and we wait for prompt
      when we search for nginx
      then we see "Official build of Nginx" printed out

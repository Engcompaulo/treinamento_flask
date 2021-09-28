FROM ubuntu:latest
RUN sudo apt-get update -y && sudo apt-get upgrade && sudo apt-get install python -y && sudo apt-get install pip -y

FROM gitpod/workspace-full:latest
LABEL maintainer "Cody Neiman <cody-neiman@cody.fun>"

RUN sudo apt update && sudo apt upgrade -yq

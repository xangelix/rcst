FROM gitpod/workspace-full-vnc
MAINTAINER Cody Neiman <cody.neiman@yale.edu>
USER gitpod

# Install custom tools, runtime, etc. using apt-get
# For example, the command below would install "bastet" - a command line tetris clone:
#
# RUN sudo apt-get -q update && \
#     sudo apt-get install -yq bastet && \
#     sudo rm -rf /var/lib/apt/lists/*
#
# More information: https://www.gitpod.io/docs/config-docker/

RUN sudo apt update && sudo apt upgrade -yq && python -m pip install --upgrade pip && \
    sudo apt -yq install debconf-utils && \
    echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections && \
    echo keyboard-configuration keyboard-configuration/layout select 'English (US)' | sudo debconf-set-selections && \
    echo keyboard-configuration keyboard-configuration/layoutcode select 'us' | sudo debconf-set-selections && \
    echo "resolvconf resolvconf/linkify-resolvconf boolean false" | sudo debconf-set-selections && \
    export DEBIAN_FRONTEND=noninteractive && sudo apt install -yq ubuntu-minimal ubuntu-standard kde-standard && \
    sudo apt install -yq rclone libnotify-bin

ENV XDG_SESSION_TYPE="x11"

FROM gitpod/workspace-full-vnc

USER gitpod

# Install custom tools, runtime, etc. using apt-get
# For example, the command below would install "bastet" - a command line tetris clone:
#
# RUN sudo apt-get -q update && \
#     sudo apt-get install -yq bastet && \
#     sudo rm -rf /var/lib/apt/lists/*
#
# More information: https://www.gitpod.io/docs/config-docker/

RUN sudo apt update && sudo apt upgrade -yq && \
    DEBIAN_FRONTEND=noninteractive sudo apt install -yq ubuntu-minimal ubuntu-standard kde-plasma-desktop && \
    sudo apt install -yq rclone

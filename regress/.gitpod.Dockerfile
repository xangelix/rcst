FROM gitpod/workspace-full:latest
MAINTAINER Cody Neiman <cody.neiman@yale.edu>

# Install Xvfb, JavaFX-helpers and Openbox window manager
RUN sudo apt-get update && \
    sudo apt-get install -yq xvfb x11vnc xterm openjfx libopenjfx-java openbox && \
    sudo rm -rf /var/lib/apt/lists/*

# Overwrite this env variable to use a different window manager
ENV WINDOW_MANAGER="openbox"

USER root

# Change the default number of virtual desktops from 4 to 1 (footgun)
RUN sed -ri "s/<number>4<\/number>/<number>1<\/number>/" /etc/xdg/openbox/rc.xml

# Install novnc
RUN git clone https://github.com/novnc/noVNC.git /opt/novnc \
    && git clone https://github.com/novnc/websockify /opt/novnc/utils/websockify
COPY novnc-index.html /opt/novnc/index.html

# Add VNC startup script
COPY start-vnc-session.sh /usr/bin/
RUN chmod +x /usr/bin/start-vnc-session.sh

# This is a bit of a hack. At the moment we have no means of starting background
# tasks from a Dockerfile. This workaround checks, on each bashrc eval, if the X
# server is running on screen 0, and if not starts Xvfb, x11vnc and novnc.
RUN echo "export DISPLAY=:0" >> ~/.bashrc
RUN echo "[ ! -e /tmp/.X0-lock ] && (/usr/bin/start-vnc-session.sh &> /tmp/display-\${DISPLAY}.log)" >> ~/.bashrc

### checks ###
# no root-owned files in the home directory
RUN notOwnedFile=$(find . -not "(" -user gitpod -and -group gitpod ")" -print -quit) \
    && { [ -z "$notOwnedFile" ] \
        || { echo "Error: not all files/dirs in $HOME are owned by 'gitpod' user & group"; exit 1; } }

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

RUN pip install black

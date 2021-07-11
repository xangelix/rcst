FROM gitpod/workspace-full:latest
LABEL maintainer "Cody Neiman <cody-neiman@cody.fun>"

SHELL ["/bin/bash", "-c"]

RUN sudo apt update -yqq && sudo apt upgrade -yqq && sudo apt install -y libgtk-3-dev

RUN sudo git clone --branch beta https://github.com/flutter/flutter.git /opt/flutter

RUN sudo chown -R gitpod /opt/flutter

RUN /opt/flutter/bin/flutter --version && \
    /opt/flutter/bin/flutter config --enable-linux-desktop && \
    /opt/flutter/bin/flutter doctor -v 

RUN echo "export PATH=$PATH:/opt/flutter/bin" >> ~/.bashrc

RUN source ~/.bashrc

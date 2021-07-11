FROM gitpod/workspace-full:latest
LABEL maintainer "Cody Neiman <cody-neiman@cody.fun>"

RUN sudo apt update && sudo apt upgrade -yq

RUN sudo git clone --branch beta https://github.com/flutter/flutter.git /workspace/flutter

RUN ../flutter/bin/flutter --version && \
    ../flutter/bin/flutter config --enable-linux-desktop && \
    ../flutter/bin/flutter doctor -v 

RUN echo "export PATH=$PATH:/workspace/flutter/bin" >> ~/.bashrc

RUN source ~/.bashrc

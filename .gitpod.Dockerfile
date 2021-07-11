FROM gitpod/workspace-full:latest
LABEL maintainer "Cody Neiman <cody-neiman@cody.fun>"

SHELL ["/bin/bash", "-c"]

RUN sudo git clone --branch beta https://github.com/flutter/flutter.git /workspace/flutter

RUN sudo chown -R gitpod /workspace/flutter/

RUN /workspace/flutter/bin/flutter --version && \
    /workspace/flutter/bin/flutter config --enable-linux-desktop && \
    /workspace/flutter/bin/flutter doctor -v 

RUN echo "export PATH=$PATH:/workspace/flutter/bin" >> ~/.bashrc

RUN source ~/.bashrc

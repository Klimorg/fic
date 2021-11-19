FROM ubuntu:20.04

ARG DEBIAN_FRONTEND="noninteractive"

WORKDIR /home/
RUN apt-get update && apt-get upgrade -y
RUN apt install python3 python3-dev python3-pip libgl1-mesa-glx libglib2.0-0 -y

# set username/id to be non root user and get same rights as in my ubuntu
ARG USERNAME=lambda
ARG USER_UID=1000
ARG USER_GID=1000

RUN groupadd -g $USER_GID -o $USERNAME
# https://forums.developer.nvidia.com/t/nvidia-docker-seems-unable-to-use-gpu-as-non-root-user/80276/5 : pourquoi rajouter le "usermod -a -G video $USERNAME"
RUN useradd -m -u $USER_UID -g $USER_GID -o -s /bin/bash $USERNAME && usermod -a -G video $USERNAME

USER $USERNAME

# RUN /usr/bin/python -m pip install --upgrade pip

COPY requirements.txt .
COPY src/ src/

# set path for python libs
ENV PATH "$PATH:/home/$USERNAME/.local/bin"

RUN /bin/bash -c "pip3 install -r requirements.txt --no-cache"

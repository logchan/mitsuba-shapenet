FROM ubuntu:18.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    scons \
    mercurial \
    qt4-dev-tools \
    libpng-dev \
    libjpeg-dev \
    libilmbase-dev \
    libxerces-c-dev \
    libboost-all-dev \
    libopenexr-dev \
    libglewmx-dev \
    libxxf86vm-dev \
    libpcrecpp0v5 \
    libeigen3-dev \
    libfftw3-dev \
    libglu1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 logchan
RUN useradd -u 1000 -g logchan logchan
RUN mkdir -p /home/logchan
RUN chown logchan:logchan /home/logchan
USER logchan

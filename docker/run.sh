#!/bin/bash

docker run -it --rm \
    -v $HOME/research/code/mitsuba-shapenet:/code \
    -v $HOME/research/data/render:/data \
    mitsuba-shapenet \
    /bin/bash

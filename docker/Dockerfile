FROM nvidia/cuda:12.3.2-cudnn9-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /

RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get install -y python3-pip python3-dev && \
    apt-get install -y wget && \
    apt-get install -y nano vim && \
    apt-get install -y zip unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p $CONDA_DIR && \
    rm ~/anaconda.sh

ENV PATH="$CONDA_DIR/bin:$PATH"

RUN /bin/bash -c "source /root/.bashrc && conda --version && conda init bash"

EXPOSE 8888

CMD ["/bin/bash"]
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-c"]

RUN apt-get clean && \
    apt update -y && \
    apt install -y \
    wget \
    vim \
    firefox \
    python3.10-dev \
    python3.10-distutils \
    curl && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.10 get-pip.py && \
    pip3.10 install --upgrade pip

WORKDIR /root

RUN mkdir datacollectionpipeline

COPY webscraper_property_sales.py ./datacollectionpipeline/
COPY requirements.txt ./datacollectionpipeline/
COPY drivers ./datacollectionpipeline/drivers

WORKDIR /root/datacollectionpipeline

RUN python3 -m pip install -r requirements.txt
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y

#CMD ["python3", "webscarper_property_sales.py"]

FROM python:3.10

WORKDIR /app

COPY app /app

RUN pip3 install --upgrade -r requirements.txt

# Ubuntu installation of Pytorch
RUN pip3 install torch --extra-index-url https://download.pytorch.org/whl/cpu

RUN git clone https://github.com/facebookresearch/esm

RUN mkdir data/esm_data

RUN mkdir data/pretrained

# Download weights in data/pretrained
RUN pip3 install gdown
RUN gdown --id 1zrEU-HPNV3wp7wLAx4KnuiVyD794Oboj
RUN apt-get update && apt-get install -y unzip
RUN unzip CLEAN_pretrained.zip -d data/pretrained

RUN python build.py install

COPY entrypoint.sh ./entrypoint.sh
CMD ["./entrypoint.sh"]

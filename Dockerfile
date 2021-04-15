#FROM python:3.8.6-alpine3.12
FROM ubuntu:20.04


ENV PYTHONUNBUFFERED=0

# Install locale
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales && \
    echo "$LANG UTF-8" >> /etc/locale.gen && \
    locale-gen && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

   # Timezone
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    python3-pip python3-venv tmux curl lnav \
    build-essential python3-dev libkrb5-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    tesseract-ocr python3-opencv

ADD forza_result/requirements.txt /tmp
RUN pip3 install --upgrade pip setuptools wheel \
    && pip install -r /tmp/requirements.txt

# ==============================================================================
RUN mkdir -p /src
ADD . /src
ADD eng.traineddata /root

# ==============================================================================
# 설치
WORKDIR /src
RUN python3 setup.py install

# ==============================================================================
# 설치파일 정리
WORKDIR /root
RUN rm -rf /src

EXPOSE 5000
ENV TESSDATA_PREFIX=/root
ENV OMP_THREAD_LIMIT=1
#CMD ["python3", "-m", "forza_result", "-a", "0.0.0.0"]
ENTRYPOINT ["forza-result-api"]

FROM ubuntu:20.04

LABEL author="Michael Schmidt"
LABEL project="Atari breakout CNN"
LABEL license="MIT"

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt update \
    && apt -y --no-install-recommends install \
        bash \
        python3 \
        python3-pip \
        wget

# Mini-conda??
#RUN mkdir -p /opt/conda
#RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.12.0-Linux-x86_64.sh -O /opt/conda/miniconda.sh \
#    && bash /opt/conda/miniconda.sh -b -p /opt/miniconda


RUN mkdir app
COPY src /app

# Mini-conda ??
# CMD ["/opt/miniconda/bin/conda", "run", "--no-capture-output", "-n", "base", "python" "breakout.py"]

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirement.txt

WORKDIR app

# Atleast have a proper shell.
CMD ["/bin/bash"]
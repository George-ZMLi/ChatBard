FROM python:3.9

WORKDIR /

COPY chatbot.py /
COPY ChatGPT.py /
COPY requirements.txt /

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV ACCESS_TOKEN=6125927916:AAEDhlGkXPBVQTekmYUAtYt3SuH_TMwGQIc
ENV HOST="chatbart.redis.cache.windows.net"
ENV PASSWORD="LDyPk3e3HDX5uR7ZL8fwf55nFeBuoxZFeAzCaM7Hw3o="
ENV REDISPORT=6380
ENV GPTAPIKEY="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"

CMD ["python", "chatbot.py"]
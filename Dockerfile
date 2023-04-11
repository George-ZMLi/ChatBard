FROM python:3.10-slim

WORKDIR /

COPY chatbot.py /
COPY ChatGPT.py /
COPY requirements.txt /
COPY fluid-dreamer-379116-0a0ed06b12dd.json /
COPY textAndspeech.py /

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "chatbot.py"]
FROM python:3.10-slim

WORKDIR /

COPY chatbot.py /
COPY ChatGPT.py /
COPY requirements.txt /

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "chatbot.py"]
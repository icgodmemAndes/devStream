FROM python:3.11
LABEL authors="Grupo11 DevStreams"
RUN groupadd -r appuser
RUN useradd -r -m -g appuser appuser
USER appuser

WORKDIR /app
COPY ./.ebextensions /app/.ebextensions
COPY ./src /app/src
COPY ./application.py /app/application.py
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "application.py"]
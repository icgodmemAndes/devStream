FROM public.ecr.aws/docker/library/python:3.11.6-slim-bookworm

RUN pip install --upgrade pip

WORKDIR /app
COPY . /app/
    
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "application.py"]

# Configuración NewRelic
RUN pip install newrelic

ENV NEW_RELIC_APP_NAME="devStream"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=c6653590744f7898b4fd16f00f47be8dFFFFNRAL
ENV NEW_RELIC_LOG_LEVEL=info

ENTRYPOINT ["newrelic-admin", "run-program"]
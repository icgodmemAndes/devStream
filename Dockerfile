FROM public.ecr.aws/docker/library/python:3.11.6-slim-bookworm

RUN pip install --upgrade pip

WORKDIR /app
COPY . /app/
    
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "application.py"]
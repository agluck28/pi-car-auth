FROM python:3.10-buster

WORKDIR /var/apps/authService

COPY requirements.service.txt .

COPY src .

RUN pip install -r requirements.service.txt --no-cache-dir

ENTRYPOINT ["python"]

CMD [ "./authService.py" ]
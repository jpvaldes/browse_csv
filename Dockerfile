FROM python:3.6-slim

ADD . /opt/app
RUN find /opt/app -name instance -exec rm -r {} \+
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /opt/app/requirements.txt
EXPOSE 5000
ENV FLASK_APP=/opt/app/browse_csv/browse_csv.py
CMD [ "flask", "run", "--host=0.0.0.0" ]

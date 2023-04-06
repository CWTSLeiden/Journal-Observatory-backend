# Base docker image, Python version
FROM python:3.11-alpine

# Install requirements
COPY ./pad_api/requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Copy application
COPY ./pad_api/src /app/src
COPY ./pad_api/start.sh /docker-entrypoint.sh

# Start application
ENV PYTHONPATH=/app/src
ENTRYPOINT ["/bin/sh", "/docker-entrypoint.sh"]
CMD ["run"]

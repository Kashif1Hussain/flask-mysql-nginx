FROM python:3.10
RUN pip install --upgrade pip

# Install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy flask files
COPY python/* .

EXPOSE 8080

# Start gunicorn as WSGI server and expose it a (Docker container internal) localhost port 8080 (which we expose above)
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "backend:app"]
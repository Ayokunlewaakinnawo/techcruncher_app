# Use the official Python image as a base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install Gunicorn using pip
RUN pip install gunicorn

# Copy the Django project into the container
COPY techcruncher/ /app

# Collect static files
RUN python manage.py collectstatic --noinput

# Create directory for static files
RUN mkdir -p /techcruncher/technews/static/

# Command to run Gunicorn
CMD ["/usr/local/bin/gunicorn", "techcruncherapp.wsgi:application", "--bind", "0.0.0.0:8000"]

FROM nginx:latest

# Copy custom Nginx configuration file to the container
COPY nginx/nginx.conf /etc/nginx/nginx.conf
# BASE IMAGE
FROM python:3.10

# UPGRADE PIP
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
    
# COPY: FILES TO SOURCE DIRECTORY
COPY . /code 

# PERMISSIONS
RUN chmod +x /code/src


# INSTALL DEPENDECIES
RUN pip install --no-cache-dir --upgrade -r code/src/requirements.txt

# EXPOSE: FASTAPI
EXPOSE 8005

# SET WORKING DIRECTORY
WORKDIR /code/src

ENV PYTHONPATH "${PYTHONPATH}:/code/src"

# Install Package (setup.py)
CMD pip install -e .
# Start from a Python OpenCV base image built on Alpine
FROM tuanictu97/python-opencv:4.9.0-alpine

# Set the working directory in the container
WORKDIR /app

RUN apk update

# Upgrade pip
RUN pip3 install --no-cache --upgrade pip setuptools

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5001
EXPOSE 5001

# Install Python dependencies from requirements.txt
RUN pip3 install --no-cache-dir --use-pep517 -r requirements.txt

# Command to run the application
CMD ["python3", "main.py"]

# Use an official Python runtime as a base image
FROM python:3.9.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for the Flask apps
EXPOSE 5500
EXPOSE 5600

# Run your Flask apps when the container launches
CMD ["python", "dataapi.py"]
CMD ["python", "constructionapi.py"]
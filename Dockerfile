# Set the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container's working directory
COPY requirements.txt .

# Install the required packages listed in requirements.txt
RUN pip install -r requirements.txt

# Copy all files from the current directory to the container's working directory
COPY . .

# Expose port 8080 for the container
EXPOSE 8080

# Set the command to run the main.py file using Python
CMD ["python", "app.py"]
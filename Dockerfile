# Use a slim Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies, ensuring PyTorch is installed for CPU
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY ./src ./src

# Define the command to run the application
# It expects the path to the input JSON file to be passed as an argument
# Example: docker run my_app ./data/collection_1/challenge1b_input.json
ENTRYPOINT ["python", "-m", "src.main"]

# Use the official HomeAssistant AddOn base image
FROM homeassistant/amd64-base:latest

# Set the working directory
WORKDIR /app

# Copy the Python script to the container
COPY main.py .

# Install Python and required dependencies
RUN apk add --no-cache python3 
#&& \
#    pip3 install -r requirements.txt

# Set the entrypoint to run the Python script
ENTRYPOINT ["python3", "main.py"]

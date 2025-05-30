# Use a lightweight Python base image
FROM python:3.13-slim

LABEL org.opencontainers.image.title="LLM-API"
LABEL org.opencontainers.image.description="A RAG LLM API"
LABEL org.opencontainers.image.vendor="Rajat Jain"
LABEL org.opencontainers.image.url="https://x.com/RajatJ17005"

# Install OS-level dependencies (wget and unzip for downloading and extracting ngrok)
RUN apt-get update && apt-get install -y curl apt-transport-https gnupg && apt-get clean

RUN curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | tee /etc/apt/sources.list.d/ngrok.list \
  && apt-get update \
  && apt-get install -y ngrok

# Set the working directory for your application
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application source code into the container
COPY . /app/

# Copy the entrypoint script to the container root and ensure it's executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port that your FastAPI app listens on
EXPOSE 8000

# Set the default command to run your entrypoint script
CMD ["/entrypoint.sh"]

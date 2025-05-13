FROM python:3.11-slim

# Set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY /bot bot
COPY .env /app/.env

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r bot/requirements.txt

ENV SETUP=docker


# Run main.py when the container launches
ENTRYPOINT ["python", "main.py"]

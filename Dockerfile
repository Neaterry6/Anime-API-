# Use an official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# ✅ Install system dependencies
RUN apt-get update && apt-get install -y python3 python3-pip wget unzip

# ✅ Copy `requirements.txt` first (Ensure it exists!)
COPY requirements.txt /app/

# ✅ Install Python dependencies
RUN pip install -r /app/requirements.txt

# ✅ Copy the full app AFTER dependencies
COPY . /app/

# Expose Flask port
EXPOSE 5000

# ✅ Start Flask app correctly
CMD ["python3", "/app/app.py"]

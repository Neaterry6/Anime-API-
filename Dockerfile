# Use an official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# ✅ Copy the full app
COPY . .

# Expose Flask port
EXPOSE 5000

# Run Flask app
CMD ["python3", "app.py"

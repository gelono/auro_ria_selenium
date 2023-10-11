FROM python:3.11

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy source code
COPY . .

WORKDIR /app

#Run the app
CMD ["python", "main.py"]

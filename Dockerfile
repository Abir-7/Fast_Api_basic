FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt /app/requirements.txt

# Install python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

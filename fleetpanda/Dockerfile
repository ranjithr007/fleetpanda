# Python runtime
FROM python:3.11-slim


# Application folder inside container
WORKDIR /app


# Install system dependencies for SQL Server ODBC
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unixodbc \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*


# Install Microsoft ODBC Driver 17
RUN curl https://packages.microsoft.com/keys/microsoft.asc \
    | gpg --dearmor \
    > /usr/share/keyrings/microsoft-prod.gpg


RUN echo "deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
    > /etc/apt/sources.list.d/mssql-release.list


RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17


# Copy requirements first (docker cache)
COPY requirements.txt .


# Install python packages
RUN pip install --no-cache-dir -r requirements.txt


# Copy application
COPY . .


# FastAPI port
EXPOSE 8000


# Start application
CMD [
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]
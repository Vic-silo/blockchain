FROM python:3.11-slim

WORKDIR /src

# Configure environment and project
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv pip install --system .

# Copy code
COPY . .

# Configure and run API
EXPOSE 8000
CMD ["uvicorn", "src.infrastructure.http.main_controller:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
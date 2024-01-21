FROM python:3.10.10-slim-buster
WORKDIR /Background-Remover
RUN apt-get update && apt-get install -y \
    libgomp1 libgl1 libsm6 libxext6 libglib2.0-0 libxrender1 \
    libpng-dev \
    build-essential cmake

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --timeout=120 -r requirements.txt
COPY . /Background-Remover
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
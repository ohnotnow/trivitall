FROM python:3.7-slim

WORKDIR /trivitall
RUN apt-get update && apt-get install -y --no-install-recommends wget apt-transport-https gnupg lsb-release && \
    wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add - && \
    echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | tee -a /etc/apt/sources.list.d/trivy.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends trivy && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt trivitall.py /trivitall/
RUN pip install -r requirements.txt
CMD ["python", "./trivitall.py"]

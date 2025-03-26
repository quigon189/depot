FROM docker.io/python:3.11-slim

WORKDIR /app
COPY . ./
RUN pip install --upgrade pip && pip install -r requirements.txt 

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 5000
CMD ["flask", "run"]
